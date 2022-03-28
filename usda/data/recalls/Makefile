# Import aliases
include ./utils/variables.make

MAKENAME = usda-recalls

# scrape: ## Scrape data files
# 	$(call start,$(MAKENAME))
# 	$(call python,./usda/scrape.py)
# 	$(call finish)

recalls_html = $(wildcard usda/data/recalls/**/*.html)
recalls_json = $(recalls_html:%.html=%.json)

#include $(subst .html,.json,$(recalls_html))

%.json: %.html
	$(call python,usda/parse_web_item.py $< $@)

parse: $(recalls_json)
	cat $(recalls_json) > usda/data/recalls/all.json

scrape:
	$(call python,usda/scrape_recalls.py usda/data/recalls)

clean:
	rm usds/data/recalls/*/*.json

all:
	parse
	scrape

.PHONY: all
	scrape
