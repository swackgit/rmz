#! python3
import requests
import os
from bs4 import BeautifulSoup
import re

rss_opening = """
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:admin="http://webns.net/mvcb/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
<channel>
<title>RapidMoviez</title>
<link>https://rmz.cr/</link>
<description>Download Movies/TV Shows from Rapidshare, Hofile, Fileserve, ...</description>
<dc:language>en-ca</dc:language>
<dc:creator>info at rapidmoviez dot com</dc:creator>
<dc:rights>Copyright 2022</dc:rights>
<admin:generatorAgent rdf:resource="http://www.codeigniter.com/"/>
"""
rss_closing = f"</channel></rss>"


def main():
    page_content = ""
    # if os.path.exists('./start.rss'):
    #     with open('start.rss', 'rb') as f:
    #         output = f.read()
    # else:
    output = requests.get(f'https://rmz.cr/feed', verify=False)
    output.raise_for_status()
        # with open('start.rss', 'wb') as f:
        #     for chunk in output.iter_content(100000):
        #         f.write(chunk)

    soup = BeautifulSoup(output.text, 'html.parser')
    items = soup.find_all('item')
    regexp = re.compile(r'\[RR.NF.CU\]')
    regexp2 = re.compile(r'480p')
    for item in items:
        title = item.find('title').text
        if regexp.search(title):
            if regexp2.search(title):
                continue
                # page_content += str(item)
            else:
                guid = item.find('guid').text
                pubdate = item.find('pubdate').text
                description = get_page_info(guid)
                page_content += "<item><title>" + title + "</title>"
                page_content += "<link>" + guid + "</link>"
                page_content += "<guid>" + guid + "</guid>"
                page_content += "<description><![CDATA[ " + str(description) + " ]]></description>"
                page_content += "<pubDate>" + pubdate + "</pubDate></item>"
        else:
            continue
            # page_content += str(item)
    make_rss(page_content)


def get_page_info(url):
    print(url)
    page_name = re.search('(https://rmz.cr/release/)(.*)', url)
    if os.path.exists(f'/var/www/python/rmz/pages/{page_name[2]}.rss'):
        with open(f'/var/www/python/rmz/pages/{page_name[2]}.rss', 'rb') as f:
            output = f.read()
        soup = BeautifulSoup(output, 'html.parser')
    else:
        output = requests.get(f'{url}', verify=False)
        output.raise_for_status()
        with open(f'/var/www/python/rmz/pages/{page_name[2]}.rss', 'wb') as f:
            for chunk in output.iter_content(100000):
                f.write(chunk)
        soup = BeautifulSoup(output.text, 'html.parser')

    page = soup.find(class_='blog-details clear')
    return page


def make_rss(content):
    with open('/var/www/html/rmz.rss', 'w', encoding="utf-8") as f:
        f.write(rss_opening)
        f.write(content)
        f.write(rss_closing)


main()

#import requests

#output = requests.get("https://rmz.cr/feed", verify=False)
#output.raise_for_status()
#with open('/var/www/html/rmz.rss', 'wb') as f:
#    for chunk in output.iter_content(100000):
#        f.write(chunk)
