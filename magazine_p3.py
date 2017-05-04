# script to download the article links and discription
# from the wired site

import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from xlwt import Workbook

output_file = "wired.xls"
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('wired')
sheet_row = 0

def download(url, num_retries=2):
    print ('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
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
    current_url = urljoin(base_url,str(i))
    print(current_url)
    html = download (current_url)

    article_section = BeautifulSoup(html, "lxml").find(attrs={'class':'col col-18 no-marg'})
    for article_list in article_section.find_all("li"):
        pub_date = article_list.time.text
        title = article_list.h2.text
        summary = article_list.p.text
        link = article_list.find("a")

        output_worksheet.write(sheet_row, 0, pub_date)
        output_worksheet.write(sheet_row, 1, title)
        output_worksheet.write(sheet_row, 2, summary)
        output_worksheet.write(sheet_row, 3, link["href"])
        sheet_row += 1


output_workbook.save(output_file)
