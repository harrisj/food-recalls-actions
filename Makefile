include ./utils/variables.make

usda:
	$(call make,usda/Makefile all)

usda_full:
	$(call make,usda/Makefile full)

all: usda

.PHONY: all    \
		usda
