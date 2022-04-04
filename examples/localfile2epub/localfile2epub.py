import os

import xml2epub

## change work dir to root of `local_file_example.html`
# os.chdir("examples/localfile2epub")
## create an empty eBook
book = xml2epub.Epub("My New E-book Name")
## create chapters by file
chapter0 = xml2epub.create_chapter_from_string("./local_file_example/03-06-OdnY0A.png", strict=False, local=True, title='Cover')  # local image as cover
chapter1 = xml2epub.create_chapter_from_file("local_file_example.html", local=True)  # images in the html are local resources
## add chapters to your eBook
book.add_chapter(chapter0)
book.add_chapter(chapter1)
## generate epub file
book.create_epub("Your Output Directory")