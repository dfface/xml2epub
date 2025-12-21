import xml2epub
import requests
from bs4 import BeautifulSoup

def get_html_string(url):
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    request_headers = {'User-Agent': user_agent}
    request_object = requests.get(url, headers=request_headers)
    request_object.encoding = 'utf-8'
    html_string = request_object.text
    # Custom Main Data
    cleaned_string = xml2epub.html_clean(html_string, tag_dictionary=None, tag_clean_list=["aside","nav", "script"], class_clean_list=["hx:print:hidden","giscus"], help_url=url)  # must add help_url
    return cleaned_string

all_urls = [
    "https://ddia.vonng.com/ch1/",
    "https://ddia.vonng.com/ch2/",
    "https://ddia.vonng.com/ch3/",
    "https://ddia.vonng.com/ch4/",
    "https://ddia.vonng.com/ch5/",
    "https://ddia.vonng.com/ch6/",
    "https://ddia.vonng.com/ch7/",
    "https://ddia.vonng.com/ch8/",
    "https://ddia.vonng.com/ch9/",
    "https://ddia.vonng.com/ch10/",
    "https://ddia.vonng.com/ch11/",
    "https://ddia.vonng.com/ch12/",
    "https://ddia.vonng.com/ch13/",
    "https://ddia.vonng.com/glossary/",
]

book = xml2epub.Epub("DDIA", creator='Martin Kleppmann')
for url in all_urls:
    html_string = get_html_string(url)
    chapter = xml2epub.create_chapter_from_string(html_string, strict=False)
    book.add_chapter(chapter)
book.create_epub("output")
