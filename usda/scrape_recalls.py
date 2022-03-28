#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import time
from typing import Optional

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


    def scrape_page(self, page_num:int):
        print(f'Scraping page {page_num}...')
        r = requests.get(f'{RECALLS_URL}?page={page_num}')
        assert r.status_code == 200, f'Status {r.status_code} received from page'

        doc = BeautifulSoup(r.content, 'html.parser')
        main = doc.find('div', class_='view__main')
        recalls = main.find_all('div', class_='view__row')

        for r in recalls:
            recall_id = r.find('span', class_='tag--active').text.strip().replace(' ', '-')
            if re.search("^PHA-", recall_id, re.IGNORECASE):
                subdir = 'PHA'
            else:
                year_search = re.search('^[0-9]+-([0-9]{4})', recall_id)
                if year_search:
                    subdir = year_search.group(1)
                else:
                    subdir = "no_year"

            print(f"  + {recall_id}")
            if not os.path.isdir(os.path.join(self.dest_dir, subdir)):
                os.mkdir(os.path.join(self.dest_dir, subdir))

            with open(os.path.join(self.dest_dir, subdir, f'{recall_id}.html'), 'w') as f:
                f.write(str(r))

    
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
