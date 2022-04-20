#!/usr/bin/env python3
from bs4 import BeautifulSoup
from usda_types import UsdaEstablishment
from datetime import datetime
import sys
import re


def parse_establishment(filename:str) -> UsdaEstablishment:
    contents = None

    with open(filename, "rb") as f:
        contents = f.read()

    doc = BeautifulSoup(contents, "html.parser")

    slug_search = re.search("/([^/]+).html$", filename)
    slug = None
    if slug_search:
        slug = slug_search.group(1)

    url = doc.find("link", {"rel": "canonical"})["href"]

    out = UsdaEstablishment(
        url=url,
        slug=slug
    )


    for meta in doc.find_all('div', class_='meta'):
        label= meta.find('span', class_='meta__label').text
        value = meta.find('span', class_='meta__value').text

        if label == 'Establishment Number':
            out.id = value
        elif label == 'Telephone':
            out.telephone = value
        elif label == 'Establishment Title/Name':
            out.name = value
        elif label == 'Grant Date':
            out.grant_date = datetime.strptime(value, '%b %d, %Y').date()
        elif label == 'Address':
            out.address = value.strip()
        elif label == 'Activities':
            out.activities = [a.strip() for a in value.split(',')]

    return out


if __name__ == '__main__':
    out = parse_establishment(sys.argv[1])
    with open(sys.argv[2], 'w') as f:
        f.write(out.json())
        f.write("\n")
