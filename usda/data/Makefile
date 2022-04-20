# Import aliases
include ./utils/variables.make

MAKENAME = usda-recalls

# scrape: ## Scrape data files
# 	$(call start,$(MAKENAME))
# 	$(call python,./usda/scrape.py)
# 	$(call finish)

recalls_html = $(wildcard usda/data/recalls/**/*.html)
recalls_json = $(recalls_html:%.html=%.json)

establishments_html = $(wildcard usda/data/establishments/*.html)
establishments_json = $(establishments_json:%.html=%.json)

#include $(subst .html,.json,$(recalls_html))

# How to haee diferent processing
%.json: %.html
	$(call python,usda/parse_web_item.py $< $@)


parse: $(establishments_json) $(recalls_json)
	echo "Done"

scrape:
	$(call python,usda/scrape_recalls.py usda/data/recalls)

clean:
	rm usda/data/**/*.json

purge:
	rm -f usda/data/**/*.html
	rm -f usda/data/**/*.json

all:
	scrape
	parse

.PHONY: all
	scrape
	purge
