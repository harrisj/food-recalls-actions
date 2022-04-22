include ./utils/variables.make

MAKENAME = usda

scrape:
	$(call make,./usda/data/recalls/Makefile scrape)

update:
	$(call make,./usda/data/recalls/Makefile update)

parse:
	$(call make,./usda/data/establishments/Makefile parse)
	$(call make,./usda/data/recalls/Makefile parse)


clean:
	$(call make,./usda/data/establishments/Makefile clean)
	$(call make,./usda/data/recalls/Makefile clean)

purge:
	$(call make,./usda/usda/data/establishments/Makefile purge)
	$(call make,./usda/data/recalls/Makefile purge)

all: 
	update
	parse

full: 
	scrape
	parse


.PHONY: all full scrape parse clean purge update
