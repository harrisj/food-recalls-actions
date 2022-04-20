#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import time
from typing import Optional
from checksum import checksum_str, checksum_file
from slugify import slugify
from urllib.parse import urljoin


RECALLS_URL = 'https://www.fsis.usda.gov/recalls'
SLEEP_INTERVAL = 4

class RecallScraper:
    def __init__(self, dest_dir:str, max_page:Optional[int]):
        self.dest_dir = dest_dir
        self.max_page = max_page


    def parse_max_page(self, doc):
        el = doc.find('a', class_='pager__link--last')
        assert el, 'Unable to find last page link in document'

        page_search = re.search('page=([0-9]+)', el['href'], re.IGNORECASE)
        assert page_search
        return int(page_search.group(1))


    def file_changed(self, dest_path:str, new_contents:str) -> bool:
        if not os.path.exists(dest_path):
            return True

        return checksum_file(dest_path) != checksum_str(bytearray(new_contents, 'utf-8'))


    def scrape_establishment(self, url:str):
        url = urljoin(RECALLS_URL, url)
        r = requests.get(url, headers = {'User-agent': 'Mozilla/5.0'})

        slug_search =  re.search("/([^/]+)$", url)
        assert slug_search
        slug = slugify(slug_search.group(1))
        if r.status_code == 403:
            return

        assert r.status_code == 200, f'HTTP status {r.status_code} received for {url}'

        doc = BeautifulSoup(r.content)
        head = doc.find('head')
        main_div = doc.find('div', class_='l-sidebar__main')
        establishments_dir = os.path.join(self.dest_dir, 'establishments')

        with open(os.path.join(establishments_dir, f'{slug}.html'), 'w') as f:
            f.write(str(head))
            f.write(str(main_div))


    
    def scrape_page(self, page_num:int):
        print(f'Scraping page {page_num}...')
        r = requests.get(f'{RECALLS_URL}?page={page_num}')
        assert r.status_code == 200, f'Status {r.status_code} received from page'

        doc = BeautifulSoup(r.content, 'html.parser')
        main = doc.find('div', class_='view__main')
        recalls = main.find_all('div', class_='view__row')

        for r in recalls:
            recall_id = slugify(r.find('span', class_='tag--active').text)
            if re.search("^PHA-", recall_id, re.IGNORECASE):
                subdir = 'PHA'
            else:
                year_search = re.search('^[0-9]+-([0-9]{4})', recall_id)
                if year_search:
                    subdir = year_search.group(1)
                else:
                    subdir = "no_year"

            dest_path = os.path.join(self.dest_dir, 'recalls', subdir, f'{recall_id}.html')
            if self.file_changed(dest_path, str(r)):
                print(f"  + {recall_id}")
                if not os.path.isdir(os.path.dirname(dest_path)):
                    os.mkdir(os.path.dirname(dest_path))

                with open(dest_path, 'w') as f:
                    f.write(str(r))

                establishment_link = r.find('span', class_="recall-teaser__establishment")
                if establishment_link and establishment_link.a:
                    self.scrape_establishment(establishment_link.a['href'])

            else:
                print(f"  - {recall_id}")

    
    def scrape_all(self):
        r = requests.get(RECALLS_URL)
        assert r.status_code == 200, f'Status {r.status_code} received from main page'

        doc = BeautifulSoup(r.content, 'html.parser')
        if self.max_page:
            max_page = self.max_page
        else:
            max_page = self.parse_max_page(doc)

        for page_num in range(max_page+1):
            self.scrape_page(page_num)
            print("Sleeping...")
            time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        max_page = int(sys.argv[2])
    else:
        max_page = None

    scraper = RecallScraper(sys.argv[1], max_page)
    scraper.scrape_all()
