include ./utils/variables.make

MAKENAME = usda

scrape:
	$(call make,./usda/data/recalls/Makefile scrape)

scrape_recent:
	$(call make,./usda/data/recalls/Makefile scrape_recent)

parse:
	$(call make,./usda/data/establishments/Makefile parse)
	$(call make,./usda/data/recalls/Makefile parse)


clean:
	$(call make,./usda/data/establishments/Makefile clean)
	$(call make,./usda/data/recalls/Makefile clean)

purge:
	$(call make,./usda/usda/data/establishments/Makefile purge)
	$(call make,./usda/data/recalls/Makefile purge)

update: scrape_recent parse

full: scrape parse

all: update

.PHONY: all full scrape scrape_recent parse clean purge update
