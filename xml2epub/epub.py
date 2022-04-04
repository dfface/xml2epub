#!usr/bin/python3
# -*- coding: utf-8 -*-

# Included modules
import os
import re
import shutil
import collections
import random
import string
import time
import tempfile
import importlib.util as imp

try:
    imp.find_spec('lxml')
    lxml_module_exists = True
    import lxml.etree
    import lxml.html
    import lxml.html.builder
except ImportError:
    lxml_module_exists = False

# Third party modules
import jinja2
from bs4 import BeautifulSoup

# Local modules
from . import chapter
from . import constants
from .cover import get_cover_image

# 去除 Warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def get_cover_image_path(html_string):
    """
    在静态资源替换之后的chapters中查找cover，找不到返回None，找到则返回src
    因为一旦 add_chapter 就实现了资源替换和字符串清理，之后 create 方法中会调用本方法
    """
    # 如果第一张图的 title 等于封面、第一张图的 href 中有 cover 关键字
    root = BeautifulSoup(html_string, 'html.parser')
    title_node = root.title
    if title_node is not None:
        title = title_node.string
        cover_include = False
        first_img = root.find('img')
        for cover_title in constants.COVER_TITLE_LIST:
            # 如果章节标题包含 封面 二字
            if first_img is not None and str(title.upper()).find(cover_title.upper()) != -1:
                cover_include = True
            # 如果第一张图的src 或 href 包含 封面 二字
            if first_img is not None and first_img.has_attr('href') and re.match(r'.*({}).*'.format(cover_title),
                                                                                 first_img['href'], re.I) is not None:
                cover_include = True
            # 如果第一张图的 class 包含 fullscreen
            if first_img is not None and first_img.has_attr('class') and 'fullscreen' in first_img['class']:
                cover_include = True
        if cover_include and first_img['src'] is not None:
            return first_img['src']


class _Mimetype(object):
    """
    Epub的 Mimetype文件 类, 写入固定内容的 minetype文件 到epub.
    """

    def __init__(self, parent_directory):
        minetype_template = os.path.join(
            constants.EPUB_TEMPLATES_DIR, 'mimetype')
        shutil.copy(minetype_template,
                    os.path.join(parent_directory, 'mimetype'))


class _ContainerFile(object):
    """
    Epub的 Container文件 类, 写入固定内容的 container.xml文件到 epub.
    """

    def __init__(self, parent_directory):
        container_template = os.path.join(
            constants.EPUB_TEMPLATES_DIR, 'container.xml')
        shutil.copy(container_template,
                    os.path.join(parent_directory, 'container.xml'))


class _EpubFile(object):
    """
    用于将chapters写入Epub的类
    """

    def __init__(self, template_file, **non_chapter_parameters):
        self.content = ''
        self.file_name = ''
        self.template_file = template_file
        self.non_chapter_parameters = non_chapter_parameters

    def write(self, file_name):
        self.file_name = file_name
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(self.content)

    def _render_template(self, **variable_value_pairs):
        def read_template():
            with open(self.template_file, 'r', encoding="utf-8") as f:
                tem = f.read()
            return jinja2.Template(tem)

        template = read_template()
        rendered_template = template.render(variable_value_pairs)
        self.content = rendered_template

    def add_chapters(self, **parameter_lists):
        if 'cover_image' in parameter_lists.keys():
            self.non_chapter_parameters['cover_image'] = parameter_lists['cover_image']
            parameter_lists.pop('cover_image')
        if 'css' in parameter_lists.keys():
            self.non_chapter_parameters['css'] = parameter_lists['css']
            parameter_lists.pop('css')
        if 'imgs' in parameter_lists.keys():
            self.non_chapter_parameters['imgs'] = parameter_lists['imgs']
            parameter_lists.pop('imgs')

        def check_list_lengths(lists):
            list_length = None
            for value in lists.values():
                # assert isinstance(value, list)
                if list_length is None:
                    list_length = len(value)
                else:
                    assert len(value) == list_length

        check_list_lengths(parameter_lists)
        template_chapter = collections.namedtuple('template_chapter',
                                                  parameter_lists.keys())
        chapters = [template_chapter(*items)
                    for items in zip(*parameter_lists.values())]
        self._render_template(chapters=chapters, **self.non_chapter_parameters)

    def get_content(self):
        return self.content


class TocHtml(_EpubFile):
    """
    Epub的 目录页面 类.
    """

    def __init__(self, template_file=os.path.join(constants.EPUB_TEMPLATES_DIR, 'toc.html'), **non_chapter_parameters):
        super(TocHtml, self).__init__(template_file, **non_chapter_parameters)

    def add_chapters(self, chapter_list):
        chapter_numbers = range(len(chapter_list))
        link_list = [str(n) + '.xhtml' for n in chapter_numbers]
        try:
            for c in chapter_list:
                t = type(c)
                assert type(c) == chapter.Chapter
        except AssertionError:
            raise TypeError('chapter_list items must be Chapter not %s',
                            str(t))
        chapter_titles = [c.title for c in chapter_list]
        super(TocHtml, self).add_chapters(title=chapter_titles,
                                          link=link_list)

    def get_content_as_element(self):
        if lxml_module_exists:
            root = lxml.html.fromstring(self.content.encode('utf-8'))
            return root
        else:
            raise NotImplementedError()


class TocNcx(_EpubFile):
    """
    Epub的 XML的导航控制文件(toc.ncx) 类 
    """

    def __init__(self, title='', uid=''):
        super(TocNcx, self).__init__(template_file=os.path.join(constants.EPUB_TEMPLATES_DIR, 'toc_ncx.xml'),
                                     title=title,
                                     uid=uid)

    def add_chapters(self, chapter_list):
        id_list = range(len(chapter_list))
        play_order_list = [n + 1 for n in id_list]
        title_list = [c.title for c in chapter_list]
        link_list = [str(n) + '.xhtml' for n in id_list]
        super(TocNcx, self).add_chapters(**{'id': id_list,
                                            'play_order': play_order_list,
                                            'title': title_list,
                                            'link': link_list
                                            })

    def get_content_as_element(self):
        if lxml_module_exists:
            root = lxml.etree.fromstring(self.content.encode('utf-8'))
            return root
        else:
            raise NotImplementedError()


class ContentOpf(_EpubFile):
    """
    Epub的 .opf 类, 包含文件清单和文件阅读顺序等.
    """

    def __init__(self, title, creator='', language='', rights='', publisher='', uid='', date=time.strftime("%Y-%m-%d")):
        super(ContentOpf, self).__init__(os.path.join(constants.EPUB_TEMPLATES_DIR, 'opf.xml'),
                                         title=title,
                                         creator=creator,
                                         language=language,
                                         rights=rights,
                                         publisher=publisher,
                                         uid=uid,
                                         date=date)

    def add_chapters(self, chapter_list):
        # 查找 cover，设定在前10章内找
        cover_image = 'img/cover.jpg'
        chapter_list_end = 10
        if len(chapter_list) < 10:
            chapter_list_end = len(chapter_list)
        for i in range(0, chapter_list_end):
            cover_path = get_cover_image_path(chapter_list[i].content)
            if cover_path is not None:
                cover_image = cover_path
                break
        # 整理 封面
        cover = {'type': chapter.get_image_type(cover_image), 'link': cover_image}
        # 整理 css ，去重
        css = []
        for c in chapter_list:
            for s in c.css:
                if s not in css:
                    css.append(s)
        # 整理 img，去重
        imgs = []
        for c in chapter_list:
            for i in c.imgs:
                if i not in imgs:
                    imgs.append(i)
        # 添加 items
        id_list = range(len(chapter_list))
        link_list = [str(n) + '.xhtml' for n in id_list]
        super(ContentOpf, self).add_chapters(cover_image=cover, css=css, imgs=imgs,
                                             **{'id': id_list, 'link': link_list})

    def get_content_as_element(self):
        if lxml_module_exists:
            root = lxml.etree.fromstring(self.content.encode('utf-8'))
            return root
        else:
            raise NotImplementedError()


class Epub(object):
    """
    表示epub的类. 包含添加chapter和输出epub文件.

    Parameters:
        title (str): epub的标题.
        creator (Option[str]): epub的作者.
        language (Option[str]): epub的语言.
        rights (Option[str]): epub的版权.
        publisher (Option[str]): epub的出版商.
        epub_dir(Option[str]): epub的中间文件生成的路径，默认使用系统的临时文件路径，也可自行指定.
    """

    def __init__(self, title, creator='dfface', language='en', rights='', publisher='dfface/xml2epub', epub_dir=None):
        self._create_directories(epub_dir)
        self.chapters = []
        self.title = title
        try:
            assert title
        except AssertionError:
            raise ValueError('title cannot be empty string')
        self.creator = creator
        self.language = language
        self.rights = rights
        self.publisher = publisher
        self.uid = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(12))
        self.current_chapter_number = None
        self._increase_current_chapter_number()
        self.toc_html = TocHtml()
        self.toc_ncx = TocNcx(
            self.title, self.uid
        )
        self.opf = ContentOpf(
            self.title, self.creator, self.language, self.rights, self.publisher, self.uid)
        self.minetype = _Mimetype(self.EPUB_DIR)
        self.container = _ContainerFile(self.META_INF_DIR)

    def _create_directories(self, epub_dir=None):
        """
        创建epub文件目录.
        """

        if epub_dir is None:
            self.EPUB_DIR = tempfile.mkdtemp()
        else:
            self.EPUB_DIR = epub_dir
        self.OEBPS_DIR = os.path.join(self.EPUB_DIR, 'OEBPS')
        self.META_INF_DIR = os.path.join(self.EPUB_DIR, 'META-INF')
        self.LOCAL_IMAGE_DIR = 'img'
        self.LOCAL_CSS_DIR = 'css'
        self.IMAGE_DIR = os.path.join(self.OEBPS_DIR, self.LOCAL_IMAGE_DIR)
        self.CSS_DIR = os.path.join(self.OEBPS_DIR, self.LOCAL_CSS_DIR)
        os.makedirs(self.OEBPS_DIR)
        os.makedirs(self.META_INF_DIR)
        os.makedirs(self.IMAGE_DIR)
        os.makedirs(self.CSS_DIR)

    def _increase_current_chapter_number(self):
        """
        增长当前章节序号.
        """

        if self.current_chapter_number is None:
            self.current_chapter_number = 0
        else:
            self.current_chapter_number += 1
        self.current_chapter_id = str(self.current_chapter_number)
        self.current_chapter_path = ''.join(
            [self.current_chapter_id, '.xhtml'])

    def add_chapter(self, c):
        """
        向epub中添加chapter. 创建各章节的xhtml文件.

        Parameters:
            c (Chapter): 要添加的chapter.
        Raises:
            TypeError: 如果添加的章节类型不对触发此 Error.
        """
        try:
            assert type(c) == chapter.Chapter
        except AssertionError:
            raise TypeError('chapter must be of type Chapter')
        chapter_file_output = os.path.join(
            self.OEBPS_DIR, self.current_chapter_path)
        c.replace_images_in_chapter(self.OEBPS_DIR)
        c.replace_css_in_chapter(self.OEBPS_DIR)
        c.write(chapter_file_output)
        self._increase_current_chapter_number()
        self.chapters.append(c)

    def create_epub(self, output_directory, epub_name=None):
        """
        从该对象中创建epub文件.

        Parameters:
            output_directory (str): Directory to output the epub file to
            epub_name (Option[str]): The file name of your epub. This should not contain
                .epub at the end. If this argument is not provided, defaults to the title of the epub.
        """
        def create_cover():
            """
            向epub中添加默认的cover.
            """
            # 查看是否已经有自定义的封面
            if self.opf.non_chapter_parameters is not None and 'cover_image' in self.opf.non_chapter_parameters.keys():
                # 上面默认的图片路径设置的是 'img/cover.jpg'
                cover_image = self.opf.non_chapter_parameters['cover_image']
                if 'link' in cover_image.keys() and cover_image['link'] != 'img/cover.jpg':
                    return
            cover = get_cover_image(title=self.title, author=self.creator, publisher=self.publisher)
            cover.save(os.path.join(self.OEBPS_DIR, 'img/cover.jpg'))

        def createTOCs_and_ContentOPF():
            """
            创建目录和opf文件等.
            """

            for epub_file, name in ((self.toc_html, 'toc.html'), (self.toc_ncx, 'toc.ncx'), (self.opf, 'content.opf'),):
                epub_file.add_chapters(self.chapters)
                epub_file.write(os.path.join(self.OEBPS_DIR, name))

        def create_zip_archive(epub_file_name):
            try:
                assert isinstance(
                    epub_file_name, str) or epub_file_name is None
            except AssertionError:
                raise TypeError('epub_name must be string or None')
            if epub_file_name is None:
                epub_file_name = self.title
            epub_file_name = ''.join(
                [c for c in epub_file_name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
            epub_name_with_path = os.path.join(output_directory, epub_file_name)
            try:
                os.remove(os.path.join(epub_name_with_path, '.zip'))
            except OSError:
                pass
            shutil.make_archive(epub_name_with_path, 'zip', self.EPUB_DIR)
            return epub_name_with_path + '.zip'

        def turn_zip_into_epub(zip_archive):
            epub_full_name = zip_archive.strip('.zip') + '.epub'
            try:
                os.remove(epub_full_name)
            except OSError:
                pass
            os.rename(zip_archive, epub_full_name)
            return epub_full_name

        createTOCs_and_ContentOPF()
        create_cover()
        epub_path = turn_zip_into_epub(create_zip_archive(epub_name))
        return epub_path
