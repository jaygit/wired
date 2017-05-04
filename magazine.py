# script to download the article links and discription
# from the wired site

import urllib2
import urlparse
from bs4 import BeautifulSoup

def download(url, num_retries=2):
    print ('Downloading:', url)
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print ('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html

base_url = "https://www.wired.com/category/magazine/page/"

first_page = 1
to_visit = set ((base_url))
visited = set()
last_page = 1387 



for i in range(first_page, last_page):
    current_url = urlparse.urljoin(base_url,str(i))
    print(current_url)
    html = download (current_url)

    article_section = BeautifulSoup(html, "html.parser").find(attrs={'class':'col col-18 no-marg'})
    for article_list in article_section.find_all("li"):
        pub_date = article_list.time.text
        print(pub_date)
        title = article_list.h2.text
        print(title)
        summary = article_list.p.text
        print(summary)
        link = article_list.find("a")
        print(link)

