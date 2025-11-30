#!usr/bin/python3
# -*- coding: utf-8 -*-

# Included modules
import math
import random
from datetime import datetime

# Third party modules
from PIL import Image, ImageFont, ImageDraw, ImageFilter

# Local modules
from .constants import COVER_FONT_PATH, COVER_COLOR_LIST

def textsize(text, font):
    """获取文字尺寸"""
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def get_cover_image(title: str, author: str, publisher: str) -> Image:
    """
    生成现代化的电子书封面
    """
    # 封面尺寸
    COVER_WIDTH, COVER_HEIGHT = 1000, 1400
    CONTENT_MARGIN = 80
    
    # 选择主色调
    cover_color_hex = COVER_COLOR_LIST[random.Random().randint(0, len(COVER_COLOR_LIST) - 1)]
    cover_color = hex_to_rgb(cover_color_hex)
    
    # 创建渐变背景
    im = create_modern_gradient(COVER_WIDTH, COVER_HEIGHT, cover_color)
    d = ImageDraw.Draw(im)
    
    # 定义安全区域（避免元素覆盖重要文本）
    safe_zones = define_safe_zones(COVER_WIDTH, COVER_HEIGHT, CONTENT_MARGIN)
    
    # 添加现代化几何元素（避开安全区域）
    draw_modern_geometric_elements(d, COVER_WIDTH, COVER_HEIGHT, cover_color, safe_zones)
    
    # 计算标题区域
    title_area_height = 500
    title_area_top = COVER_HEIGHT * 0.4
    title_area = (
        CONTENT_MARGIN, 
        title_area_top,
        COVER_WIDTH - CONTENT_MARGIN, 
        title_area_top + title_area_height
    )
    
    # 作者区域
    author_area_top = title_area[3] + 30
    author_area = (
        CONTENT_MARGIN,
        author_area_top,
        COVER_WIDTH - CONTENT_MARGIN,
        author_area_top + 60
    )
    
    # 出版社区域
    publisher_area = (
        CONTENT_MARGIN - 600, 
        COVER_HEIGHT - 60, 
        COVER_WIDTH - CONTENT_MARGIN, 
        COVER_HEIGHT - 20
    )
    
    # 日期区域（右下角）
    date_area = (
        COVER_WIDTH - 200,
        COVER_HEIGHT - 60,
        COVER_WIDTH - CONTENT_MARGIN,
        COVER_HEIGHT - 20
    )
    
    # 顶部横幅区域
    banner_area = (
        0, 0, COVER_WIDTH, 80
    )
    
    # 文字颜色
    text_color = get_contrasting_color(cover_color)
    author_color = adjust_color_brightness(text_color, 0.8)
    
    # 绘制顶部横幅
    draw_top_banner(d, banner_area, cover_color, text_color, author)
    
    # 绘制大标题
    title_font_size = draw_modern_title(d, title, title_area, text_color, cover_color)
    
    # 绘制作者信息
    author_font_size = draw_modern_author(d, author, author_area, author_color, title_font_size)
    
    # 绘制出版社信息
    draw_publisher_info(d, publisher, publisher_area, author_color, author_font_size)
    
    # 绘制日期
    draw_date_info(d, date_area, author_color, author_font_size)
    
    return im

def define_safe_zones(width, height, margin):
    """定义安全区域，避免几何元素覆盖重要文本"""
    safe_zones = []
    
    # 顶部横幅区域
    safe_zones.append((0, 0, width, 100))
    
    # 标题区域（扩大范围）
    safe_zones.append((margin-20, height*0.35, width-margin+20, height*0.65))
    
    # 作者区域
    safe_zones.append((margin-20, height*0.65, width-margin+20, height*0.75))
    
    # 底部区域（出版社和日期）
    safe_zones.append((0, height-100, width, height))
    
    return safe_zones

def is_point_in_safe_zone(x, y, safe_zones):
    """检查点是否在安全区域内"""
    for zone in safe_zones:
        if zone[0] <= x <= zone[2] and zone[1] <= y <= zone[3]:
            return True
    return False

def is_element_in_safe_zone(x, y, size, safe_zones):
    """检查元素是否与安全区域重叠"""
    # 检查元素的四个角
    points = [
        (x - size, y - size),  # 左上
        (x + size, y - size),  # 右上
        (x - size, y + size),  # 左下
        (x + size, y + size)   # 右下
    ]
    
    for point in points:
        if is_point_in_safe_zone(point[0], point[1], safe_zones):
            return True
    
    return False

def draw_top_banner(draw, banner_area, banner_color, text_color, author):
    """绘制顶部横幅 - 突出背景颜色"""
    # 使用更深的颜色或对比色来突出横幅背景
    # 方法1: 使用比主色调更深的颜色
    darker_banner_color = adjust_color_brightness(banner_color, 0.7)
    
    # 方法2: 或者使用互补色来创造对比
    # 计算互补色
    complementary_color = (
        255 - banner_color[0],
        255 - banner_color[1], 
        255 - banner_color[2]
    )
    
    # 随机选择一种突出方式
    if random.random() > 0.5:
        # 使用深色版本
        banner_bg_color = darker_banner_color
    else:
        # 使用互补色
        banner_bg_color = complementary_color
    
    # 绘制横幅背景
    draw.rectangle(banner_area, fill=banner_bg_color)
    
    # 横幅文字
    banner_font = ImageFont.truetype(COVER_FONT_PATH, 28)
    banner_text = f"{author}'s E-BOOK COLLECTION"
    
    # 计算文字位置（居中）
    text_width = textsize(banner_text, banner_font)[0]
    center_x = (banner_area[0] + banner_area[2]) // 2
    center_y = (banner_area[1] + banner_area[3]) // 2
    
    # 根据背景色调整文字颜色确保可读性
    banner_text_color = get_contrasting_color(banner_bg_color)
    
    # 绘制文字
    draw.text(
        (center_x, center_y),
        text=banner_text, fill=banner_text_color, anchor='mm', font=banner_font
    )
    
    # 添加装饰线条
    line_margin = 40
    line_y = center_y
    line_length = 80
    
    # 左边线条
    draw.line([
        (line_margin, line_y),
        (line_margin + line_length, line_y)
    ], fill=banner_text_color, width=2)
    
    # 右边线条
    draw.line([
        (banner_area[2] - line_margin - line_length, line_y),
        (banner_area[2] - line_margin, line_y)
    ], fill=banner_text_color, width=2)

def draw_date_info(draw, date_area, text_color, author_font_size):
    """绘制日期信息"""
    # 日期字体大小为出版社字体大小，不超过作者字体的三分之二
    date_font_size = max(24, author_font_size * 0.66)
    date_font = ImageFont.truetype(COVER_FONT_PATH, date_font_size)
    
    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m")
    
    # 绘制日期（右对齐）
    center_y = (date_area[1] + date_area[3]) // 2
    draw.text(
        (date_area[2], center_y),
        text=current_date, fill=text_color, anchor='rm', font=date_font
    )

def hex_to_rgb(hex_color):
    """将十六进制颜色转换为RGB元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_contrasting_color(color):
    """根据背景色返回对比度高的文字颜色"""
    luminance = (0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]) / 255
    return (255, 255, 255) if luminance < 0.6 else (0, 0, 0)

def adjust_color_brightness(color, factor):
    """调整颜色亮度"""
    r, g, b = color
    return (
        max(0, min(255, int(r * factor))),
        max(0, min(255, int(g * factor))),
        max(0, min(255, int(b * factor)))
    )

def create_modern_gradient(width, height, base_color):
    """创建现代化渐变背景"""
    # 生成协调的渐变色
    hue_shift = random.uniform(-0.1, 0.1)
    sat_factor = random.uniform(0.8, 1.2)
    
    # 主色和辅助色
    main_color = base_color
    accent_color = shift_color_hue(base_color, hue_shift)
    accent_color = adjust_color_saturation(accent_color, sat_factor)
    
    # 创建基础背景
    im = Image.new("RGB", (width, height), main_color)
    
    # 添加径向渐变效果
    center_x, center_y = width // 2, height // 3
    max_radius = max(width, height)
    
    for y in range(height):
        for x in range(width):
            # 计算到中心的距离
            dist = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            # 归一化距离
            norm_dist = min(dist / max_radius, 1.0)
            
            # 根据距离混合颜色
            r = int(main_color[0] * (1 - norm_dist) + accent_color[0] * norm_dist)
            g = int(main_color[1] * (1 - norm_dist) + accent_color[1] * norm_dist)
            b = int(main_color[2] * (1 - norm_dist) + accent_color[2] * norm_dist)
            
            im.putpixel((x, y), (r, g, b))
    
    # 添加轻微模糊效果使渐变更平滑
    im = im.filter(ImageFilter.GaussianBlur(2))
    
    return im

def shift_color_hue(color, hue_shift):
    """轻微调整颜色色相"""
    r, g, b = [x / 255.0 for x in color]
    
    # 简单的色相调整
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    if max_val != min_val:
        # 增加随机性但保持协调
        new_r = min(1.0, max(0.0, r + hue_shift * (1 - r)))
        new_g = min(1.0, max(0.0, g + hue_shift * (1 - g)))
        new_b = min(1.0, max(0.0, b + hue_shift * (1 - b)))
        
        return (int(new_r * 255), int(new_g * 255), int(new_b * 255))
    
    return color

def adjust_color_saturation(color, factor):
    """调整颜色饱和度"""
    r, g, b = color
    # 转换为灰度
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    
    # 调整饱和度
    r = int(gray + factor * (r - gray))
    g = int(gray + factor * (g - gray))
    b = int(gray + factor * (b - gray))
    
    return (
        max(0, min(255, r)),
        max(0, min(255, g)),
        max(0, min(255, b))
    )

def draw_modern_geometric_elements(draw, width, height, base_color, safe_zones=None):
    """绘制现代化几何元素 - 考虑安全区域"""
    if safe_zones is None:
        safe_zones = []
        
    # 生成协调的辅助色
    accent_color = shift_color_hue(base_color, 0.2)
    accent_color = adjust_color_brightness(accent_color, 1.3)
    
    # 半透明颜色
    semi_accent = (*accent_color, 150)
    semi_base = (*base_color, 100)
    
    # 1. 大背景圆形元素（避开安全区域）
    circle_radius = min(width, height) * 0.4
    circle_x = width * 0.7
    circle_y = height * 0.3
    
    # 检查圆形是否与安全区域重叠
    if not is_element_in_safe_zone(circle_x, circle_y, circle_radius, safe_zones):
        draw.ellipse(
            [circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius],
            fill=semi_base, outline=None
        )
    
    # 2. 多样化的多边形元素（避开安全区域）
    num_polygons = random.randint(5, 12)
    polygons_drawn = 0
    attempts = 0
    max_attempts = 50  # 防止无限循环
    
    while polygons_drawn < num_polygons and attempts < max_attempts:
        # 随机位置，尝试避开安全区域
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        size = random.randint(50, 120)
        
        # 检查是否在安全区域内
        if not is_element_in_safe_zone(x, y, size, safe_zones):
            draw_diverse_polygon(draw, width, height, accent_color, polygons_drawn, x, y)
            polygons_drawn += 1
        
        attempts += 1
    
    # 3. 线条元素（避开安全区域）
    draw_modern_lines(draw, width, height, base_color, safe_zones)
    
    # 4. 点状纹理（避开安全区域）
    draw_texture_dots(draw, width, height, accent_color, safe_zones)


def draw_diverse_polygon(draw, width, height, color, index, x=None, y=None):
    """绘制多样化的多边形 - 接受指定位置"""
    # 如果未指定位置，随机生成
    if x is None:
        x = random.randint(100, width - 100)
    if y is None:
        y = random.randint(100, height - 100)
        
    # 更多种类的多边形
    poly_types = [
        'triangle', 'hexagon', 'rectangle', 'blob', 
        'star', 'diamond', 'trapezoid', 'pentagon',
        'octagon', 'cross', 'wave', 'spiral'
    ]
    
    poly_type = random.choice(poly_types)
    
    # 半透明颜色，增加透明度变化
    alpha = random.randint(50, 200)
    poly_color = (*color, alpha)
        
    if poly_type == 'triangle':
        # 三角形
        size = random.randint(60, 180)
        rotation = random.uniform(0, math.pi * 2)
        
        points = []
        for i in range(3):
            angle = rotation + 2 * math.pi * i / 3
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'hexagon':
        # 六边形
        size = random.randint(50, 120)
        rotation = random.uniform(0, math.pi)
        
        points = []
        for i in range(6):
            angle = rotation + 2 * math.pi * i / 6
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'rectangle':
        # 旋转矩形
        size_x = random.randint(80, 200)
        size_y = random.randint(40, 100)
        angle = random.uniform(0, math.pi)
        
        points = []
        for dx, dy in [(-size_x/2, -size_y/2), (size_x/2, -size_y/2), 
                      (size_x/2, size_y/2), (-size_x/2, size_y/2)]:
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            points.append((x + rx, y + ry))
        
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'star':
        # 五角星
        size = random.randint(40, 100)
        outer_radius = size
        inner_radius = size * 0.4
        rotation = random.uniform(0, math.pi)
        
        points = []
        for i in range(10):
            angle = rotation + 2 * math.pi * i / 10
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'diamond':
        # 菱形
        size = random.randint(60, 150)
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y)
        ]
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'trapezoid':
        # 梯形
        width_top = random.randint(60, 120)
        width_bottom = random.randint(80, 160)
        height_trap = random.randint(40, 100)
        
        points = [
            (x - width_top/2, y - height_trap/2),
            (x + width_top/2, y - height_trap/2),
            (x + width_bottom/2, y + height_trap/2),
            (x - width_bottom/2, y + height_trap/2)
        ]
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'pentagon':
        # 五边形
        size = random.randint(50, 120)
        rotation = random.uniform(0, math.pi)
        
        points = []
        for i in range(5):
            angle = rotation + 2 * math.pi * i / 5
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'octagon':
        # 八边形
        size = random.randint(50, 100)
        rotation = random.uniform(0, math.pi)
        
        points = []
        for i in range(8):
            angle = rotation + 2 * math.pi * i / 8
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'cross':
        # 十字形
        size = random.randint(40, 80)
        width = random.randint(15, 30)
        
        # 横条
        draw.rectangle([
            x - size, y - width/2,
            x + size, y + width/2
        ], fill=poly_color)
        
        # 竖条
        draw.rectangle([
            x - width/2, y - size,
            x + width/2, y + size
        ], fill=poly_color)
        
    elif poly_type == 'wave':
        # 波浪形
        amplitude = random.randint(20, 50)
        wavelength = random.randint(80, 150)
        points = []
        
        for i in range(20):
            px = x + i * wavelength / 20
            py = y + amplitude * math.sin(i * 2 * math.pi / 10)
            points.append((px, py))
            
            if i == 19:  # 闭合形状
                points.append((px, y + amplitude + 20))
                points.append((x, y + amplitude + 20))
        
        if len(points) >= 3:
            draw.polygon(points, fill=poly_color)
        
    elif poly_type == 'spiral':
        # 螺旋形（简化版）
        center_x, center_y = x, y
        points = []
        turns = 2
        max_radius = random.randint(30, 70)
        
        for i in range(50):
            angle = 2 * math.pi * turns * i / 50
            radius = max_radius * i / 50
            px = center_x + radius * math.cos(angle)
            py = center_y + radius * math.sin(angle)
            points.append((px, py))
        
        # 螺旋形用线条绘制
        if len(points) > 1:
            draw.line(points, fill=poly_color, width=3)
    
    else:  # blob - 不规则形状
        radius = random.randint(50, 120)
        points = []
        
        num_points = random.randint(6, 10)
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            var_radius = radius * random.uniform(0.6, 1.4)
            px = x + var_radius * math.cos(angle)
            py = y + var_radius * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, fill=poly_color)

def draw_modern_lines(draw, width, height, color, safe_zones=None):
    """绘制现代化线条元素 - 考虑安全区域"""
    if safe_zones is None:
        safe_zones = []
        
    line_color = (*color, 120)
    
    # 水平线条（避开安全区域）
    for i in range(3):
        y_pos = height * 0.2 + i * 80
        
        # 检查是否在安全区域内
        in_safe_zone = False
        for zone in safe_zones:
            if zone[1] <= y_pos <= zone[3]:
                in_safe_zone = True
                break
                
        if not in_safe_zone:
            draw.line([(width * 0.1, y_pos), (width * 0.9, y_pos)], 
                     fill=line_color, width=2)
    
    # 放射状线条（中心点避开安全区域）
    center_x, center_y = width * 0.3, height * 0.7
    if not is_point_in_safe_zone(center_x, center_y, safe_zones):
        for i in range(8):
            angle = 2 * math.pi * i / 8
            length = random.randint(100, 200)
            end_x = center_x + length * math.cos(angle)
            end_y = center_y + length * math.sin(angle)
            
            # 检查终点是否在安全区域
            if not is_point_in_safe_zone(end_x, end_y, safe_zones):
                draw.line([(center_x, center_y), (end_x, end_y)], 
                         fill=line_color, width=1)

def draw_texture_dots(draw, width, height, color, safe_zones=None):
    """绘制点状纹理 - 考虑安全区域"""
    if safe_zones is None:
        safe_zones = []
        
    dot_color = (*color, 60)
    dots_drawn = 0
    attempts = 0
    max_attempts = 300  # 防止无限循环
    
    while dots_drawn < 200 and attempts < max_attempts:
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        
        # 检查是否在安全区域内
        if not is_point_in_safe_zone(x, y, safe_zones):
            draw.ellipse([x, y, x + size, y + size], fill=dot_color)
            dots_drawn += 1
        
        attempts += 1

def draw_modern_title(draw, title, title_area, text_color, bg_color):
    """绘制现代化大标题 - 修正位置计算"""
    title_width = title_area[2] - title_area[0]
    title_height = title_area[3] - title_area[1]
    
    # 寻找合适的字体大小
    final_font_size = 40
    final_lines = []
    
    for font_size in range(120, 40, -8):
        title_font = ImageFont.truetype(COVER_FONT_PATH, font_size)
        lines = wrap_text_optimized(title, title_font, title_width * 0.9)
        
        # 计算总高度
        line_height = textsize("A", title_font)[1] * 1.3
        total_height = len(lines) * line_height
        
        if total_height <= title_height * 0.8:
            final_font_size = font_size
            final_lines = lines
            final_line_height = line_height
            break
    
    # 如果没有找到合适的，使用最小字体
    if not final_lines:
        title_font = ImageFont.truetype(COVER_FONT_PATH, final_font_size)
        final_lines = wrap_text_optimized(title, title_font, title_width * 0.9)
        final_line_height = textsize("A", title_font)[1] * 1.3
    
    # 计算实际文本高度
    total_text_height = len(final_lines) * final_line_height
    
    # 计算标题背景 - 基于实际文本尺寸
    padding = 30
    text_start_y = title_area[1] + (title_height - total_text_height) / 2
    
    # 背景区域精确计算
    bg_top = text_start_y - padding
    bg_bottom = text_start_y + total_text_height + padding
    bg_left = title_area[0] - padding
    bg_right = title_area[2] + padding
    
    # 确保背景在合理范围内
    bg_top = max(bg_top, title_area[1] - 20)
    bg_bottom = min(bg_bottom, title_area[3] + 20)
    
    # 为标题添加背景增强可读性
    if text_color == (255, 255, 255):  # 白色文字需要深色背景
        title_bg_color = (*adjust_color_brightness(bg_color, 0.3), 180)
    else:  # 黑色文字需要浅色背景
        title_bg_color = (*adjust_color_brightness(bg_color, 1.8), 180)
    
    # 绘制标题背景
    draw.rectangle(
        [bg_left, bg_top, bg_right, bg_bottom],
        fill=title_bg_color
    )
    
    # 绘制标题文字
    title_font = ImageFont.truetype(COVER_FONT_PATH, final_font_size)
    for i, line in enumerate(final_lines):
        y_pos = text_start_y + i * final_line_height
        
        # 文字阴影（增强可读性）
        shadow_color = (0, 0, 0, 80) if text_color == (255, 255, 255) else (255, 255, 255, 80)
        draw.text(
            (title_area[0] + title_width/2 + 2, y_pos + 70  + 2),
            text=line, anchor='mm', fill=shadow_color, font=title_font
        )
        
        # 主要文字
        draw.text(
            (title_area[0] + title_width/2, y_pos + 70),
            text=line, anchor='mm', fill=text_color, font=title_font
        )
    
    return final_font_size

def wrap_text_optimized(text, font, max_width):
    """优化文本换行"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = textsize(test_line, font)[0]
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            # 处理长单词
            if textsize(word, font)[0] > max_width:
                lines.extend(split_long_word(word, font, max_width))
                current_line = []
            else:
                current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def split_long_word(word, font, max_width):
    """分割过长的单词"""
    lines = []
    current_chars = ""
    
    for char in word:
        test_chars = current_chars + char
        if textsize(test_chars, font)[0] <= max_width:
            current_chars = test_chars
        else:
            if current_chars:
                lines.append(current_chars)
            current_chars = char
    
    if current_chars:
        lines.append(current_chars)
    
    return lines

def draw_modern_author(draw, author, author_area, text_color, title_font_size):
    """绘制现代化作者信息"""
    # 作者字体大小为标题的一半，但限制在合理范围内
    author_font_size = max(48, min(48, title_font_size // 2))
    author_font = ImageFont.truetype(COVER_FONT_PATH, author_font_size)
    
    # 简单的作者文字，去掉装饰线
    center_y = (author_area[1] + author_area[3]) // 2
    author_text = f"by {author}"
    
    # 绘制作者文字
    draw.text(
        ((author_area[0] + author_area[2]) // 2, center_y),
        text=author_text, fill=text_color, anchor='mm', font=author_font
    )

    return author_font_size

def draw_publisher_info(draw, publisher, publisher_area, text_color, author_font_size):
    """绘制出版社信息"""
    publisher_font = ImageFont.truetype(COVER_FONT_PATH, max(24, author_font_size * 0.66))
    center_y = (publisher_area[1] + publisher_area[3]) // 2
    
    draw.text(
        ((publisher_area[0] + publisher_area[2]) // 2, center_y),
        text=publisher, fill=text_color, anchor='mm', font=publisher_font
    )