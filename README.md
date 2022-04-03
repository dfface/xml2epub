# xml2epub

![GitHub Repo stars](https://img.shields.io/github/stars/dfface/xml2epub)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dfface/xml2epub/Upload%20to%20PIP)
[![python](https://img.shields.io/pypi/pyversions/xml2epub)](https://pypi.org/project/xml2epub/)
[![pypi](https://img.shields.io/pypi/v/xml2epub)](https://pypi.org/project/xml2epub/)
[![wheel](https://img.shields.io/pypi/wheel/xml2epub)](https://pypi.org/project/xml2epub/)
[![license](https://img.shields.io/github/license/dfface/xml2epub)](https://pypi.org/project/xml2epub/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/xml2epub)

Batch convert multiple web pages into one e-book by URL, xml string, etc.

Features:
* Automatically generate cover: If the `<title>` text in html is one of [COVER_TITLE_LIST](./xml2epub/constants.py), 
then the cover will be added automatically, otherwise the default cover will be generated. We will randomly generate the cover image with a similar "O'Reilly" style.
* Automatically obtain the core content of the article: we filter the obtained html string and retain the core content. See [SUPPORTED_TAGS](./xml2epub/constants.py) for a list of tags reserved in html.

## ToC

* [How to install](#how-to-install)
* [Basic Usage](#basic-usage)
* [API](#api)
* [Tips](#tips)
* [FAQ](#faq)

## How to install

`xml2epub` is available on pypi
https://pypi.org/project/xml2epub/

```
$ pip install xml2epub
```

## Basic Usage

```python
import xml2epub

## create an empty eBook
book = xml2epub.Epub("My New E-book Name")
## create chapters by url
#### custom your own cover image
chapter0 = xml2epub.create_chapter_from_string("https://cdn.jsdelivr.net/gh/dfface/img0@master/2022/02-10-0R7kll.png", title='cover', strict=False)
#### create chapter objects
chapter1 = xml2epub.create_chapter_from_url("https://dev.to/devteam/top-7-featured-dev-posts-from-the-past-week-h6h")
chapter2 = xml2epub.create_chapter_from_url("https://dev.to/ks1912/getting-started-with-docker-34g6")
## add chapters to your eBook
book.add_chapter(chapter0)
book.add_chapter(chapter1)
book.add_chapter(chapter2)
## generate epub file
book.create_epub("Your Output Directory")
```

After waiting for a while, if no error is reported, the following "My New E-book Name.epub" file will be generated in "Your Output Directory":

![The generated epub file](https://cdn.jsdelivr.net/gh/dfface/img0@master/2022/02-09-Guz0bl.png)

For more **examples**, see: [examples](./examples) directory.

If we cannot infer the cover image from html string, we will generate one. The randomly generated cover image is a similar "O'Reilly" style: 

![The generated cover image](https://cdn.jsdelivr.net/gh/dfface/img0@master/2022/02-10-0R7kll.png)

## API

* `create_chapter_from_file(file_name, url=None, title=None, strict=True)`: Create a Chapter object from an html or xhtml file.
  * file_name (string): The filename containing the html or xhtml content of the created chapter.
  * url (Option[string]): The url used to infer the chapter title. It is recommended to bring the `url` parameter, which helps to identify relative links in the web page.
  * title (Option[string]): The chapter name of the chapter, if None, the content of the title tag obtained from the web file will be used as the chapter name.
  * strict (Option[boolean]): Whether to perform strict page cleaning, which will remove inline styles, insignificant attributes, etc., generally True.
  * local (Option[boolean]):  Whether to use local resources, which means that all images and css files in html have been saved locally, and the resources will be copied directly using the file path in html instead of getting them from the Internet.
* `create_chapter_from_url(url, title=None, strict=True)`: Create a Chapter object by extracting webpage from given url.
  * url (string): website link. It is recommended to bring the `url` parameter, which helps to identify relative links in the web page.
  * title (Option[string]): The chapter name of the chapter, if None, the content of the title tag obtained from the web file will be used as the chapter name.
  * strict (Option[boolean]): Whether to perform strict page cleaning, which will remove inline styles, insignificant attributes, etc., generally True. When False, you can enter an image link and specify title, which is helpful for custom cover image.
  * local (Option[boolean]):  Whether to use local resources, which means that all images and css files in html have been saved locally, and the resources will be copied directly using the file path in html instead of getting them from the Internet.
* `create_chapter_from_string(html_string, url=None, title=None, strict=True)`: Create a Chapter object from a string. The principle of the above two methods is to first obtain the html or xml string, and then call this method. 
  * html_string (string): html or xhtml string.
  * url (Option[string]): The url used to infer the chapter title. It is recommended to bring the `url` parameter, which helps to identify relative links in the web page.
  * title (Option[string]): The chapter name of the chapter, if None, the content of the title tag obtained from the web file will be used as the chapter name.
  * strict (Option[boolean]): Whether to perform strict page cleaning, which will remove inline styles, insignificant attributes, etc., generally True.
  * local (Option[boolean]):  Whether to use local resources, which means that all images and css files in html have been saved locally, and the resources will be copied directly using the file path in html instead of getting them from the Internet.
* `Epub(title, creator='dfface', language='en', rights='', publisher='dfface', epub_dir=None)`: Constructor method to create Epub object.Mainly used to add book information and all chapters and generate epub file.
  * title (str): The [title](http://kb.daisy.org/publishing/docs/epub/title.html) of the epub.
  * creator (Option[str]): The [author](http://kb.daisy.org/publishing/docs/html/dpub-aria/doc-credit.html) of the epub.
  * language (Option[str]): The [language](http://kb.daisy.org/publishing/docs/epub/language.html) of the epub.
  * rights (Option[str]): The [copyright](http://kb.daisy.org/publishing/docs/html/dpub-aria/doc-credit.html) of the epub.
  * publisher (Option[str]): The [publisher](http://kb.daisy.org/publishing/docs/html/dpub-aria/doc-credit.html) of the epub.
  * epub_dir(Option[str]): The path of intermediate file, the system's temporary file path is used by default, or you can specify it yourself.
* Epub object  `add_chapter(chapter_object)`: Add Chapter object to Epub.
  * chapter_object (Chapter object): Use the three methods of creating a chapter object to get the object.
* Epub object  `create_epub(output_directory, epub_name=None)`: Create an epub file from the Epub object.
  * output_directory (str): Directory to output the epub file to.
  * epub_name (Option[str]): The file name of your epub. This should not contain .epub at the end. If this argument is not provided, defaults to the title of the epub.
* `html_clean(input_string, help_url=None, tag_clean_list=constants.TAG_DELETE_LIST, class_list=constants.CLASS_INCLUDE_LIST, tag_dictionary=constants.SUPPORTED_TAGS)`: The internal default `clean` method we expose for easy customization.
  * input_string (str): A string representing HTML / XML.
  * help_url (Option[str]): current chapter's url, which helps to identify relative links in the web page.
  * tag_dictionary (Option[dict]):  defines all tags and their classes that need to be saved, you can see what the default values are in [SUPPORTED_TAGS](./xml2epub/constants.py).
  * tag_clean_list (Option[list]): defines all tags that need to be deleted. Note that the entire tag and its sub-tags will be deleted directly here. You can see what the default values are in [TAG_DELETE_LIST](./xml2epub/constants.py).
  * class_list (Option[list]): defines all tags containing the content of the class that need to be deleted, that is, as long as the class attribute of any tag contains the content in this list, then the entire tag will be deleted including its sub-tags. You can see what the default values are in [CLASS_INCLUDE_LIST](./xml2epub/constants.py).

## Tips

* If you want to add a cover image yourself, use the `create_chapter_from_string` method, then assign `html_string` to the image URL (e.g. `https://www.xxx.com/xxx.png`) and keep the `strict=False` parameter. Or assign `html_string` to the local image file path (e.g. `./xxx.png`) and keep the `local=True` and `strict=False` parameters.
* If you want to clean the web content yourself, first use the crawler to get the html string, then use the exposed `html_clean` method (it is recommended to add the values of `tag_clean_list`, `class_clean_list` and `url`) and assign the output to the `create_chapter_from_string` method `html_string` parameter while keeping `strict=False`.
* No matter which method, when using `create_chapter_*` and `strict=False` , it is recommended to bring the `url` parameter, which helps to identify relative links in the web page.
* Whenever you use the `html_clean` method, it is recommended to include the `help_url` parameter, which helps to identify relative links in web pages.
* After generating the epub, it is better to use [calibre](https://calibre-ebook.com/) to convert the `epub` to a more standards-compliant `epub`/`mobi`/`azw3` to solve the problem that the epub cannot be read in some software. And if the generated epub has style problems, you can also use calibre to edit the ebook and **adjust the style** to suit your reading habits.
* If the images and CSS files in your html are local resources, please set the `local` parameter in `create_chapter_*` to `True`, then the program will automatically copy the local resources instead of getting them from the Internet.

## FAQ

1. The generated epub has no content?
> When generating an epub by URL, you need to ensure that the web page corresponding to the URL is a static web page, and you can access all the content without logging in. If the epub you generate is empty when opened, then you may have encountered a website that requires login to access. At this time, you can try to obtain the html string corresponding to the URL, and then use the `create_chapter_from_string` method to generate the epub. That is to say, you need to use a certain crawler technology.
2. The generated epub contains content I don't want?
> Although we do some filtering when cleaning the html string, this is not guaranteed to work in all cases. In this case, I recommend that you filter the html string yourself before using `create_chapter_from_string` method.
3. Want to generate epub directly from html string without sanitizing content?
> Set the parameter `strict` of `create_chapter_from_string` to `False`, which means that it will not be cleaned up internally.
4. If you choose to get the html string yourself and clean it up yourself, you can follow these steps:
   1. Use crawler technology to obtain html strings, such as `requests.get(url).text`.
   2. Use the `html_clean` method we expose to clean up the string, e.g. `html_clean(html_string, tag_clean_list=['sidebar'])`. Or you can write your own methods to sanitize strings, all just to get clean strings, whatever you want.
   3. Using the `create_chapter_from_string(html_string, strict=False)` method to generate the Chapter object, pay special attention to the parameter `` to be set to False, which means that our internal cleaning strategy will be skipped.
   4. After that, you can generate epub according to the basic usage. See [vuepress2epub.py](examples/vuepress2epub/vuepress2epub.py) as an example.