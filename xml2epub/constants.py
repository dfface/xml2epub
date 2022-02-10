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
    'img': ['align', 'border', 'height', 'id', 'src', 'width'],
    'img /': ['align', 'border', 'height', 'id', 'src', 'width'],
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
