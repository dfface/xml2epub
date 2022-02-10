#!usr/bin/python3
# -*- coding: utf-8 -*-

# Included modules
import math
import os
import random
import re

# Third party modules
from PIL import Image, ImageFont, ImageDraw

# Local modules
from .constants import ANIMAL_PIC_DIR, COVER_FONT_PATH, COVER_COLOR_LIST


def get_cover_image(title: str, author: str, publisher: str) -> Image:
    """
    生成 Cover Image
    """
    # contants
    TITLE_RECTANGLE_TUPLE = (100, 835, 900, 1165)  # 标题文字的box
    TITLE_BG_RECTANGLE_TUPLE = (50, 800, 950, 1200)  # 标题背景的box
    # animal pic
    animal_names = os.listdir(ANIMAL_PIC_DIR)
    random_animal_name = animal_names[random.Random().randint(0, len(animal_names) - 1)]
    animal = Image.open(os.path.join(ANIMAL_PIC_DIR, random_animal_name))
    animal = animal.resize((int(500), int(animal.height * 500 / animal.width)))  # 保证宽500
    # cover color
    cover_color = COVER_COLOR_LIST[random.Random().randint(0, len(COVER_COLOR_LIST) - 1)]
    # fonts
    title_font = ImageFont.truetype(COVER_FONT_PATH, 96)
    author_font = ImageFont.truetype(COVER_FONT_PATH, 48)
    publisher_font = ImageFont.truetype(COVER_FONT_PATH, 32)
    im = Image.new("RGB", (1000, 1400), "white")  # 书籍封面图片底色
    d = ImageDraw.Draw(im)
    im.paste(animal, (450, 175))  # 动物
    d.rectangle(TITLE_BG_RECTANGLE_TUPLE, fill=cover_color)  # 标题背景方框
    d.rectangle((50, 0, 950, 50), fill=cover_color)  # 页眉方框
    # 作者名字的描写
    author_text_size = d.textsize(text=author, font=author_font)
    if TITLE_BG_RECTANGLE_TUPLE[2] - author_text_size[0] >= TITLE_BG_RECTANGLE_TUPLE[0]:
        author_text_start = TITLE_BG_RECTANGLE_TUPLE[2] - author_text_size[0]
    else:
        author_text_start = TITLE_BG_RECTANGLE_TUPLE[0]
    d.text((author_text_start, 1220), text=author, fill='black', anchor='lt', font=author_font)
    # 标题的描写
    title_text_size = d.textsize(text=title, font=title_font)
    title_rec_size = TITLE_RECTANGLE_TUPLE[2] - TITLE_RECTANGLE_TUPLE[0]
    if title_text_size[0] > title_rec_size:
        # 一行写不下必须分行
        full_len = int(title_rec_size / title_text_size[0] * len(title))  # 一行最多写几个字
        lines = re.findall(".{" + str(full_len) + "}", title)
        if len(''.join(lines)) < len(title):
            lines.append(title[len(''.join(lines)):])
        title_one_word_size = d.textsize(text=title[0], font=title_font)
        par_space = 20  # 段落间距
        actual_line_num = math.floor((TITLE_RECTANGLE_TUPLE[3] - TITLE_RECTANGLE_TUPLE[1]) / (title_one_word_size[1] + par_space))
        if actual_line_num > len(lines):
            actual_line_num = len(lines)
        for i in range(actual_line_num):
            d.text((500, TITLE_RECTANGLE_TUPLE[1] + i * (title_one_word_size[1] + par_space)), text=lines[i], anchor='ma', fill="white", font=title_font)
    else:
        d.text((500, (TITLE_BG_RECTANGLE_TUPLE[1] + TITLE_BG_RECTANGLE_TUPLE[3]) / 2), anchor='ms', text=title, fill="white", font=title_font)
    # 出版商的描写
    d.text((50, 1300), text=publisher, fill=cover_color, anchor='lt', font=publisher_font)
    # 页眉的描写
    header_text_size = d.textsize(text=f"{author}'s ebook series", font=publisher_font)
    d.text((500, 50 + header_text_size[1]), text=f"{author}'s ebook series", fill=cover_color, anchor='mm', font=publisher_font)
    return im
