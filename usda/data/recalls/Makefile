# Import aliases
include ./utils/variables.make

MAKENAME = usda-recalls

# scrape: ## Scrape data files
# 	$(call start,$(MAKENAME))
# 	$(call python,./usda/scrape.py)
# 	$(call finish)

recalls_html = $(wildcard usda/data/recalls/**/*.html)
recalls_json = $(recalls_html:%.html=%.json)

%.json: %.html
	$(call python,usda/parse_recall.py --src=$< --dest=$@ --establishments=usda/data/establishments)

usda/recalls.ndjson: $(recalls_json)
	cat usda/data/recalls/**/*.json > usda/recalls.ndjson

usda/recalls.csv: usda/recalls.ndjson
	$(call python,usda/recalls_json_to_csv.py --json=$< --csv=$@)

parse: usda/recalls.csv

scrape:
	$(call python,usda/scrape_recalls.py usda/data)

scrape_recent:
	$(call python,usda/scrape_recalls.py usda/data 3)

clean:
	rm =f usda/data/recalls/**/*.json

purge:
	rm -f usda/data/recalls/**/*.html
	rm -f usda/data/recalls/**/*.json

all: scrape_recent parse

.PHONY: all scrape scrape_recent parse update
