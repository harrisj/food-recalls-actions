include ./utils/variables.make

usda:
	$(call make,usda/Makefile)

all:
	usda

.PHONY: all    \
		usda
