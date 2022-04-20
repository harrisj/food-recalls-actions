include ./utils/variables.make

MAKENAME = usda-establishments

establishments_html = $(wildcard usda/data/establishments/*.html)
establishments_json = $(establishments_html:%.html=%.json)

%.json: %.html
	$(call python,usda/parse_establishment.py $< $@)

parse: $(establishments_json)
	cat usda/data/establishments/*.json > usda/establishments.ndjson

clean:
	rm -f usda/data/establishments/*.json

purge:
	rm -f usda/data/establishments/*.json
	rm -f usda/data/establishments/*.html

all: parse

.PHONY: all clean purge parse
