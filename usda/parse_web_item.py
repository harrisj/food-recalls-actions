#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
from usda_types import UsdaRecall, RiskLevel

BASE_FSIS_URL = 'https://www.fsis.usda.gov/'

def parse_fsis_row(filename:str) -> UsdaRecall:
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")

        id = soup.find("span", class_="tag--active").text
        title_element = soup.find("h3", class_="recall-teaser__title").a
        url = urljoin(BASE_FSIS_URL, title_element['href'])
        reasons=[a.text for a in soup.findAll("a", class_="tag--reason")]
        status=soup.find("div", class_="recall-teaser__status").span.text

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
            status=status
        )

        return out


if __name__ == "__main__":
    out = parse_fsis_row(sys.argv[1])

    with open(sys.argv[2], 'w') as f:
        f.write(out.json())
