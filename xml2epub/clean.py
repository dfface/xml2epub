#!usr/bin/python3
# -*- coding: utf-8 -*-

# Included modules
import re

# Third party modules
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Local modules
from . import constants


def relative_url_replace(tag, help_url):
    """
    将网页中的相对链接（如 '/assets/a.jpg' ），替换为绝对链接（如 'https://www.a.com/assets/a.jpg'）
        help_url: 当前页面的 url
        tag：当前的 bs 元素
    """
    if help_url is None:
        return tag
    href_urls = tag.find_all(lambda x: x.has_attr('href'))
    src_urls = tag.find_all(lambda x: x.has_attr('src'))
    for i in href_urls:
        if urlparse(i['href']).scheme == '':
            if urlparse(help_url).scheme == '':
                break
            else:
                if str(i['href']).startswith('/'):
                    i['href'] = urljoin(urlparse(help_url).scheme + '://' + urlparse(help_url).netloc, i['href'])
                elif str(i['href']).startswith('#'):
                    continue
                else:
                    i['href'] = urljoin(help_url, i['href'])
    for i in src_urls:
        if urlparse(i['src']).scheme == '':
            if urlparse(help_url).scheme == '':
                break
            else:
                if str(i['src']).startswith('/'):
                    i['src'] = urljoin(urlparse(help_url).scheme + '://' + urlparse(help_url).netloc, i['src'])
                else:
                    i['src'] = urljoin(help_url, i['src'])
    return tag


def create_html_from_fragment(tag):
    """
    Creates full html tree from a fragment. Assumes that tag should be wrapped in a body and is currently not

    Parameters:
        tag: a bs4.element.Tag

    Returns:"
        bs4.element.Tag: A bs4 tag representing a full html document
    """

    try:
        assert isinstance(tag, bs4.element.Tag)
    except AssertionError:
        raise TypeError
    try:
        assert tag.find_all('body') == []
    except AssertionError:
        raise ValueError

    soup = BeautifulSoup(
        '<html><head></head><body></body></html>', 'html.parser')
    soup.body.append(tag)
    return soup


def clean(input_string, help_url=None, title=None,
          tag_dictionary=constants.SUPPORTED_TAGS,
          tag_clean_list=constants.TAG_DELETE_LIST,
          class_list=constants.CLASS_INCLUDE_LIST):
    """
    Sanitizes HTML. Tags not contained as keys in the tag_dictionary input are
    removed, and child nodes are recursively moved to parent of removed node.
    Attributes not contained as arguments in tag_dictionary are removed.
    Doctype is set to <!DOCTYPE html>.

    Parameters:
        input_string (basestring): A (possibly unicode) string representing HTML.
        help_url (Option[str]): 当前页面的 url ，用于辅助替换页面中所有的相对资源
        tag_dictionary (Option[dict]): A dictionary with tags as keys and
            attributes as values. This operates as a whitelist--i.e. if a tag
            isn't contained, it will be removed. By default, this is set to
            use the supported tags and attributes for the Amazon Kindle,
            as found at https://kdp.amazon.com/help?topicId=A1JPUWCSD6F59O
        class_list (Option[list]): 清理class属性中可能包含该列表中关键字的所有元素及其子元素
        tag_clean_list (Option[list]): 清理该列表中包含的所有 tag 元素及其子元素

    Returns:
        str: A (possibly unicode) string representing HTML.

    Raises:
        TypeError: Raised if input_string isn't a unicode string or string.
    """
    try:
        assert isinstance(input_string, str)
    except AssertionError:
        raise TypeError
    # 使用 lxml 更为准确和严格，默认不保存 link 元素，可自定义删除的tag
    root = BeautifulSoup(input_string, 'lxml')
    title = root.find('title')  # 暴露出该方法后，防止后面直接提取article的时候title丢失，该方法会执行两次
    # 如果能找到 article 元素，直接提取该元素
    article_tag = root.find_all('article')
    if article_tag:
        root = article_tag[0]
        if title:
            root.insert_before(title)
    # 删除 class_list 中的元素及其子元素，例如导航栏、边栏等元素及其子元素
    for i in class_list:
        to_delete = root.find_all(lambda tag: tag.has_attr('class') and str(tag['class']).find(i) != -1)
        for td in to_delete:
            td.extract()
    # 删除 tag_clean_list 中包含的所有 tag 及其子元素
    for i in tag_clean_list:
        to_delete = root.find_all(i)
        for td in to_delete:
            td.extract()
    # 仅保留 tag_dictionary 中的元素，子元素可保存
    stack = root.find_all(True, recursive=False)
    while stack:
        current_node = stack.pop()
        child_node_list = current_node.find_all(True, recursive=False)
        if current_node.name not in tag_dictionary.keys():
            parent_node = current_node.parent
            current_node.extract()
            for n in child_node_list:
                parent_node.append(n)
        else:
            attribute_dict = current_node.attrs
            for attribute in list(attribute_dict.keys()):
                if attribute not in tag_dictionary[current_node.name]:
                    attribute_dict.pop(attribute)
        stack.extend(child_node_list)
    # 删除无用的 <link>
    for i in root.find_all('link'):
        if (i.has_attr('rel') and i['rel'][0] == 'stylesheet') or \
                (i.has_attr('type') and i['type'][0] == 'text/css') or (
                not i.has_attr('type') and not i.has_attr('rel')):
            continue
        else:
            i.extract()
    # 删除不是 head 中的 <link>
    for i in root.find_all('link'):
        for j in i.find_parents():
            if j.name == 'body':
                i.extract()
                break
    # 相对资源的替换
    root = relative_url_replace(root, help_url)
    # 懒加载图片资源的替换
    all_imgs = root.find_all('img')
    for i in all_imgs:
        if i.has_attr('data-src') and not i.has_attr('src'):
            i['src'] = i['data-src']
    # wrap partial tree if necessary
    if not root.find_all('html'):
        root = create_html_from_fragment(root)
    # Remove img tags without src attribute
    image_node_list = root.find_all('img')
    for node in image_node_list:
        if not node.has_attr('src'):
            node.extract()
    unformatted_html_unicode_string = root.prettify()
    # fix <br> tags since not handled well by default by bs4
    unformatted_html_unicode_string = unformatted_html_unicode_string.replace(
        '<br>', '<br/>')
    # remove &nbsp; and replace with space since not handled well by certain e-readers
    unformatted_html_unicode_string = unformatted_html_unicode_string.replace(
        '&nbsp;', ' ')
    return unformatted_html_unicode_string


def clean_not_strict(input_string, help_url=None, title=None):
    """
    直接保留原 html ，因为原 html 足够合适
    如果 Input_string 是图片，则直接插入图片，于是可以利用这个特性手动添加第一页的封面
        input_string: html、image_url、image_file_path
        help_url (Option[str]): 当前页面的 url ，用于辅助替换页面中所有的相对资源
    """
    try:
        assert isinstance(input_string, str)
    except AssertionError:
        raise TypeError
    is_img = False
    for ending in ['jpg', 'jpeg', 'gif', 'png']:
        if input_string.endswith(ending):
            is_img = True
    if is_img:
        root = create_html_from_fragment(BeautifulSoup(f'<img src="{input_string}" />', 'html.parser').img)
        title_tag = root.new_tag(name='title')
        if title is not None:
            title_tag.string = title
        else:
            title_tag.string = 'cover'
        root.find('head').append(title_tag)
    else:
        root = BeautifulSoup(input_string, 'html.parser')
        if not root.find_all('html'):
            root = create_html_from_fragment(root)
    # 相对资源的替换
    root = relative_url_replace(root, help_url)
    unformatted_html_unicode_string = root.prettify()
    unformatted_html_unicode_string = unformatted_html_unicode_string.replace(
        '<br>', '<br/>')
    unformatted_html_unicode_string = unformatted_html_unicode_string.replace(
        '&nbsp;', ' ')
    return unformatted_html_unicode_string


def condense(input_string):
    """
    Trims leadings and trailing whitespace between tags in an html document

    Parameters:
        input_string: A (possible unicode) string representing HTML.

    Returns:
        A (possibly unicode) string representing HTML.

    Raises:
        TypeError: Raised if input_string isn't a unicode string or string.
    """
    try:
        assert isinstance(input_string, str)
    except AssertionError:
        raise TypeError
    removed_leading_whitespace = re.sub(r'>\s+', '>', input_string).strip()
    removed_trailing_whitespace = re.sub(
        r'\s+<', '<', removed_leading_whitespace).strip()
    return removed_trailing_whitespace


def html_to_xhtml(html_unicode_string):
    """
    Converts html to xhtml

    Parameters:
        html_unicode_string: A (possible unicode) string representing HTML.

    Returns:
        A (possibly unicode) string representing XHTML.

    Raises:
        TypeError: Raised if input_string isn't a unicode string or string.
    """
    try:
        assert isinstance(html_unicode_string, str)
    except AssertionError:
        raise TypeError
    root = BeautifulSoup(html_unicode_string, 'html.parser')
    # Confirm root node is html
    try:
        assert root.html is not None
    except AssertionError:
        raise ValueError(''.join(['html_unicode_string cannot be a fragment.',
                                  'string is the following: %s', root]))
    # Add xmlns attribute to html node
    root.html['xmlns'] = 'http://www.w3.org/1999/xhtml'
    unicode_string = root.prettify()
    # Close singleton tag_dictionary
    for tag in constants.SINGLETON_TAG_LIST:
        unicode_string = unicode_string.replace(
            '<' + tag + '/>',
            '<' + tag + ' />')
    return unicode_string


def html_clean(input_string, help_url=None,
               tag_clean_list=constants.TAG_DELETE_LIST,
               class_clean_list=constants.CLASS_INCLUDE_LIST,
               tag_dictionary=constants.SUPPORTED_TAGS):
    """
    Sanitizes HTML / XML. Tags not contained as keys in the tag_dictionary input are
    removed, and child nodes are recursively moved to parent of removed node.
    Attributes not contained as arguments in tag_dictionary are removed.
    Doctype is set to <!DOCTYPE html>.

    Tips:
        1. Generally, you only need to delete the tags you don't need, you only need to customize the tag_clean_list,
        and the others can be kept by default.
        2. tag_dictionary defines all tags and their classes that need to be saved, you can see what the default values
         are.
        3. tag_clean_list defines all tags that need to be deleted. Note that the entire tag and its sub-tags will be
         deleted directly here.
        4. class_list defines all tags containing the content of the class that need to be deleted, that is, as long
         as the class attribute of any tag contains the content in this list, then the entire tag will be deleted
          including its sub-tags.

    Parameters:
        input_string (basestring): A (possibly unicode) string representing HTML.
        help_url (Option[str]): 当前页面的 url ，用于辅助替换页面中所有的相对资源.
        tag_dictionary (Option[dict]): A dictionary with tags as keys and
            attributes as values. This operates as a whitelist--i.e. if a tag
            isn't contained, it will be removed. By default, this is set to
            use the supported tags and attributes for the Amazon Kindle,
            as found at https://kdp.amazon.com/help?topicId=A1JPUWCSD6F59O. 定义了需要保存的所有tag及其class，
            你可以看看默认值都有什么。
        class_list (Option[list]): defines all tags containing the content of the class that need to be deleted, that
            is, as long as the class attribute of any tag contains the content in this list, then the entire tag will
            be deleted including its sub-tags. 清理class属性中可能包含该列表中关键字的所有元素及其子元素。
        tag_clean_list (Option[list]): defines all tags that need to be deleted. Note that the entire tag and its
            sub-tags will be deleted directly here. 清理该列表中包含的所有 tag 元素及其子元素。

    Returns:
        str: A (possibly unicode) string representing HTML.

    Raises:
        TypeError: Raised if input_string isn't a unicode string or string.
    """
    html_string = clean(input_string, help_url=help_url, tag_dictionary=tag_dictionary, tag_clean_list=tag_clean_list, class_list=class_clean_list)
    return html_to_xhtml(html_string)
