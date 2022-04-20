#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup
from typing import Optional
import sys
import requests
from urllib.parse import urljoin
from usda_types import UsdaRecall, UsdaEstablishment, RiskLevel
from datetime import date, datetime
from slugify import slugify
import re
import os


BASE_FSIS_URL = 'https://www.fsis.usda.gov/'

def element_text(soup: BeautifulSoup, element_name:str, class_:str) -> Optional[str]:
    element = soup.find(element_name, class_=class_)
    if element:
        return element.text
    else:
        return None


def load_establishment(url:str, establishments_dir:str) -> Optional[UsdaEstablishment]:
    slug_search = re.search('/([^/]+)$', url)
    if not slug_search:
        return None

    slug = slugify(slug_search.group(1))
    path = os.path.join(establishments_dir, f'{slug}.json')
    if not os.path.exists(path):
        return None

    with open(path, 'r') as f:
        print(f"   Establishment: {slug}")
        return UsdaEstablishment.parse_raw(f.read())

    
def parse_fsis_row(filename:str, establishments:str) -> UsdaRecall:
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")

        id = element_text(soup, "span", "tag--active")
        title_element = soup.find("h3", class_="recall-teaser__title").a
        url = urljoin(BASE_FSIS_URL, title_element['href'])
        reasons=[a.text for a in soup.findAll("a", class_="tag--reason")]
        status=soup.find("div", class_="recall-teaser__status").span.text
        summary=element_text(soup, "div", "recall-teaser__summary")

        risk_level = None
        if soup.find('a', class_="tag--high"):
            risk_level = RiskLevel.HIGH
        elif soup.find('a', class_="tag--low"):
            risk_level = RiskLevel.LOW
        elif soup.find('a', class_="tag--marginal"):
            risk_level = RiskLevel.MARGINAL

        out = UsdaRecall(
            id=id,
            title=title_element.text,
            url=url,
            risk_level=risk_level,
            reasons=reasons,
            status=status,
            summary=summary
        )

        date_str = element_text(soup, "div", "recall-teaser__date")
        if date_str:
            start_date_search = re.search("(Mon|Tue|Wed|Thu|Fri|Sat|Sun), ([0-9]{2}/[0-9]{2}/[0-9]{4}) -", date_str)
            if start_date_search:
                out.start_date = datetime.strptime(start_date_search.group(2), '%m/%d/%Y').date()

            end_date_search = re.search("- (Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([0-9]{2}/[0-9]{2}/[0-9]{4})", date_str)
            if end_date_search:
                out.end_date = datetime.strptime(end_date_search.group(2), '%m/%d/%Y').date()

        for ptag in soup.find_all('div', 'recall-teaser__products'):
            tag_title = ptag.h5.text
            if tag_title == 'Impacted Products':
                out.impacted_products = [span.text for span in ptag.find_all('span')]
            elif tag_title == 'Quantity Recovered':
                quantity_text = ptag.text.strip()
                qsearch = re.search('([0-9,]+) (.*)$', quantity_text)
                if qsearch:
                    out.quantity_recovered = int(qsearch.group(1).replace(',', ''))
                    out.quantity_unit = qsearch.group(2)

        states_list = element_text(soup, 'div', 'recall-teaser__states')
        if states_list:
            out.states = [state.strip() for state in states_list.split(',')]

        establishment_link = soup.find('span', class_="recall-teaser__establishment")
        if establishment_link and establishment_link.a:
            out.establishment = load_establishment(establishment_link.a['href'], establishments)

        return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a recall file')
    parser.add_argument('--src', type=str, help='The src HTML snippet')
    parser.add_argument('--dest', type=str, help='The destination JSON file')
    parser.add_argument('--establishments', type=str, help="Where the establishment directory is")
    args = parser.parse_args()

    out = parse_fsis_row(args.src, args.establishments)
    with open(args.dest, 'w') as f:
        f.write(out.json())
        f.write("\n")
