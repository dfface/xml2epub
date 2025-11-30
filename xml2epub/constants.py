#!usr/bin/python3
# -*- coding: utf-8 -*-

import os

SUPPORTED_TAGS = {
    'a': ['href', 'id', 'name', 'class'],
    'b': ['id'],
    'big': [],
    'blockquote': ['id'],
    'body': [],
    'br': ['id'],
    'center': [],
    'cite': [],
    'code': [],
    'dd': ['id', 'title'],
    'del': [],
    'dfn': [],
    'div': ['align', 'id', 'bgcolor', 'class'],
    'em': ['id', 'title'],
    'font': ['color', 'face', 'id', 'size'],
    'head': [],
    'h1': ['id'],
    'h2': ['id'],
    'h3': ['id'],
    'h4': ['id'],
    'h5': ['id'],
    'h6': ['id'],
    'hr /': ['color', 'id', 'width'],
    'html': [],
    'i': ['class', 'id'],
    'img': ['align', 'border', 'height', 'id', 'src', 'width', 'data-src'],
    'img /': ['align', 'border', 'height', 'id', 'src', 'width', 'data-src'],
    'li': ['class', 'id', 'title'],
    'link': ['type', 'rel', 'href'],
    'ol': ['id'],
    'p': ['align', 'id', 'title'],
    'pre': ['class'],
    's': ['id', 'style', 'title'],
    'small': ['id'],
    'span': ['bgcolor', 'title', 'class'],
    'strike': ['class', 'id'],
    'strong': ['class', 'id'],
    'style': ['type'],
    'sub': ['id'],
    'sup': ['class', 'id'],
    'table': ['class', 'id', 'title'],
    'tbody': [],
    'td': [],
    'th': [],
    'thead': ['id'],
    'title': [],
    'tr': [],
    'u': ['id'],
    'ul': ['class', 'id'],
    'var': []
}
SINGLETON_TAG_LIST = [
    'area',
    'base',
    'br',
    'col',
    'command',
    'embed',
    'hr',
    'img',
    'input',
    'link',
    'meta',
    'param',
    'source',
]
CLASS_INCLUDE_LIST = [
    'side'
    'nav',
    'hidden',
    'hide',
    'edit',
    'audio',
    'video',
]
TAG_DELETE_LIST = [
    'aside',
    'nav',
    'link',
]
COVER_TITLE_LIST = [
    'cover', 'cover-image', 'ci', '封面', 'カバー', 'couverture',
    'Startseite', 'trải ra', 'ปิดบัง', '씌우다', 'обложка', 'التغطية'
]
xhtml_doctype_string = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EPUB_TEMPLATES_DIR = os.path.join(BASE_DIR, 'epub_templates')
ANIMAL_PIC_DIR = os.path.join(BASE_DIR, "epub_cover/animals")
COVER_FONT_PATH = os.path.join(BASE_DIR, "epub_cover/LXGWWenKai-Regular.ttf")
COVER_COLOR_LIST = [
    '#c04851',
    '#5a1216',
    '#f1939c',
    '#7a7374',
    '#ee4866',
    '#621d34',
    '#681752',
    '#ad6598',
    '#1e131d',
    '#525288',
    '#2177b8',
    '#619ac3',
    '#baccd9',
    '#2f90b9',
    '#1ba784',
    '#57c3c2',
    '#2bae85',
    '#1a6840',
    '#add5a2',
    '#5e5314',
    '#fbda41',
    '#d2b42c',
    '#fecc11',
    '#f8d86a',
    '#b78d12',
    '#daa45a',
    '#fa7e23',
    '#f8b37f',
    '#f2481b',
    '#f33b1f',
    '#ac1f18',
    '#483332',
    '#4b2e2b',
    
    # 现代蓝色系 (10种)
    "#1a73e8",  # 活力蓝
    "#4285f4",  # 谷歌蓝
    "#2962ff",  # 材料设计蓝
    "#00bcd4",  # 青蓝色
    "#03a9f4",  # 亮蓝色
    "#2196f3",  # 材料蓝
    "#1976d2",  # 深蓝
    "#1565c0",  # 经典蓝
    "#0d47a1",  # 午夜蓝
    "#82b1ff",  # 浅天蓝
    
    # 优雅紫色系 (8种)
    "#7b1fa2",  # 深紫色
    "#9c27b0",  # 紫罗兰
    "#673ab7",  # 深紫蓝
    "#3f51b5",  # 靛蓝色
    "#6200ea",  # 电紫色
    "#aa00ff",  # 紫红色
    "#e040fb",  # 兰花紫
    "#7c4dff",  # 浅紫
    
    # 自然绿色系 (8种)
    "#0f9d58",  # 翡翠绿
    "#43a047",  # 森林绿
    "#009688",  # 蓝绿色
    "#4caf50",  # 材料绿
    "#2e7d32",  # 深绿
    "#00c853",  # 亮绿
    "#64dd17",  # 酸橙绿
    "#388e3c",  # 深翡翠绿
    
    # 温暖橙色/红色系 (8种)
    "#ff5722",  # 深橙色
    "#f4511e",  # 南瓜橙
    "#e64a19",  # 深红橙
    "#d32f2f",  # 深红色
    "#ff5252",  # 珊瑚红
    "#ff1744",  # 亮红色
    "#dd2c00",  # 深红
    "#ff6d00",  # 亮橙色
    
    # 中性/大地色系 (8种)
    "#795548",  # 棕色
    "#607d8b",  # 蓝灰色
    "#455a64",  # 深蓝灰
    "#37474f",  # 炭灰蓝
    "#546e7a",  # 石板灰
    "#8d6e63",  # 陶土色
    "#a1887f",  # 浅棕色
    "#5d4037",  # 深棕色
    
    # 粉色/珊瑚色系 (4种)
    "#e91e63",  # 粉红色
    "#ad1457",  # 深粉红
    "#ec407a",  # 亮粉红
    "#f8bbd0",  # 浅粉红
    
    # 金色/黄色系 (4种)
    "#fbc02d",  # 金黄色
    "#f57f17",  # 琥珀色
    "#ffa000",  # 琥珀橙
    "#ffd600"   # 亮黄色
]
