import requests
import time
import xml2epub
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# ebook settings
EBOOK_NAME = "Tomcat & MyBatis Tutorial"
OUTPUT_DIR = "Your Output Directory"
# website specific settings
start_urls = [
    'https://www.pdai.tech/md/framework/tomcat/tomcat-x-design-web-container.html',
]
tag_to_remove = [
    'footer'
]
class_to_remove = [
    'side',
    'nav'
]

## create an empty eBook
book = xml2epub.Epub(EBOOK_NAME, creator='pdai')
## do html cleanning yourself
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
request_headers = {'User-Agent': user_agent}
s = requests.session()
s.headers.update(request_headers)

for start_url in start_urls:
    request_object = s.get(start_url)
    request_object.encoding = 'utf-8'
    html_string = request_object.text
    soup = BeautifulSoup(html_string, 'lxml')
    # add new urls we found in html_string
    urls = []
    for i in soup.find_all("a", class_="sidebar-link"):
        new_url = urljoin(urlparse(start_url).scheme + "://" + urlparse(start_url).netloc, i['href'])
        if new_url != start_url:
            urls.append(new_url)
    print(f"Total: {len(urls)}")
    ## use the exposed html_clean method
    cleaned_string = xml2epub.html_clean(html_string, tag_clean_list=tag_to_remove, class_clean_list=class_to_remove, help_url=start_url)  # must add help_url
    cleaned_chapter = xml2epub.create_chapter_from_string(cleaned_string, strict=False)  # must be False
    ## add chapter to Epub object
    book.add_chapter(cleaned_chapter)
    # handle new urls
    for i, url in enumerate(urls):
        print(str(i + 1) + " " + str(url))
        request_object = s.get(url)
        request_object.encoding = 'utf-8'
        html_string = request_object.text
        cleaned_string = xml2epub.html_clean(html_string, tag_clean_list=tag_to_remove, class_clean_list=class_to_remove, help_url=url)  # must add help_url
        cleaned_chapter = xml2epub.create_chapter_from_string(cleaned_string, strict=False)  # must be False
        book.add_chapter(cleaned_chapter)
        time.sleep(5)

s.close()
## generate epub file
book.create_epub(OUTPUT_DIR)
