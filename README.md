# xml2epub

![GitHub Repo stars](https://img.shields.io/github/stars/dfface/xml2epub)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dfface/xml2epub/Upload%20to%20PIP)
[![python](https://img.shields.io/pypi/pyversions/xml2epub)](https://pypi.org/project/xml2epub/)
[![pypi](https://img.shields.io/pypi/v/xml2epub)](https://pypi.org/project/xml2epub/)
[![wheel](https://img.shields.io/pypi/wheel/xml2epub)](https://pypi.org/project/xml2epub/)
[![license](https://img.shields.io/github/license/dfface/xml2epub)](https://pypi.org/project/xml2epub/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/xml2epub)

Batch convert multiple web pages into one e-book by URL, xml string, etc.

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
chapter1 = xml2epub.create_chapter_from_url("https://dev.to/devteam/top-7-featured-dev-posts-from-the-past-week-h6h")
chapter2 = xml2epub.create_chapter_from_url("https://dev.to/ks1912/getting-started-with-docker-34g6")
## add chapters to your eBook
book.add_chapter(chapter1)
book.add_chapter(chapter2)
## generate epub file
book.create_epub("Your Output Directory")
```

After waiting for a while, if no error is reported, the following "My New E-book Name.epub" file will be generated in "Your Output Directory":

![The generated epub file](https://cdn.jsdelivr.net/gh/dfface/img0@master/2022/02-09-Guz0bl.png)

## API

* `create_chapter_from_file(file_name, url=None, title=None, strict=True)`: Create a Chapter object from an html or xhtml file.
  * file_name (string): The filename containing the html or xhtml content of the created chapter.
  * url (Option[string]): The url used to infer the chapter title.
  * title (Option[string]): The chapter name of the chapter, if None, the content of the title tag obtained from the web file will be used as the chapter name.
  * strict （Option[boolean]): Whether to perform strict page cleaning, which will remove inline styles, insignificant attributes, etc., generally True.
* `create_chapter_from_url(url, title=None, strict=True)`: Create a Chapter object by extracting webpage from given url.
  * url (string): website link.
  * title (Option[string]): The chapter name of the chapter, if None, the content of the title tag obtained from the web file will be used as the chapter name.
  * strict （Option[boolean]): Whether to perform strict page cleaning, which will remove inline styles, insignificant attributes, etc., generally True.
* `create_chapter_from_string(html_string, url=None, title=None, strict=True)`: Create a Chapter object from a string. The principle of the above two methods is to first obtain the html or xml string, and then call this method.
  * html_string (string): html or xhtml string.
  * url (Option[string]): The url used to infer the chapter title.
  * title (Option[string]): The chapter name of the chapter, if None, the content of the title tag obtained from the web file will be used as the chapter name.
  * strict （Option[boolean]): Whether to perform strict page cleaning, which will remove inline styles, insignificant attributes, etc., generally True.
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