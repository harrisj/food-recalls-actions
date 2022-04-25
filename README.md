# food-recalls-scraper

An experiment in using Github actions to scrape food recall data. Currently this
is just pulling data from the USDA (meat, poultry and egg) since the USDA does
not provide bulk data in an accessible format. In the future, it might also pull
data from the FDA, but that is provided in a better raw format.

This scraper is mainly a chance for me to get my feet wet writing scrapers with Python, orchestrating them with make and running them in Github Actions. I am indebted (and in some cases literally stole code from) the previous works of [Ben Welsh](https://palewi.re/who-is-ben-welsh/), specifically:

* [First GitHub Scraper](https://github.com/palewire/first-github-scraper) 
* [News Homepages](https://github.com/palewire/news-homepages)
* [California Coronavirus Scrapers](https://github.com/datadesk/california-coronavirus-scrapers)

## USDA FSIS Scraper

The USDA scraper pulls data from the [USDA Food Safety and Inspection Service website](https://www.fsis.usda.gov/) about recalls for meat, poultry and eggs. These are grabbed as web snippets from the [recalls page](https://www.fsis.usda.gov/recalls) as web snippets, which are then analyzed with Python scripts to produce JSON snippets. These snippets are then merged into large [newline-delimited JSON files](http://ndjson.org/) which are converted by another script into a CSV file.

Although the recalls themselves link to press releases, I do not grab the text of those. That could be added as a future enhancement however.

### Where Data is Located

All of the data for the scrapers are located in the `usda/data` directory under the following structure:

* [establishments.json](usda/establishments.json) - a ND-JSON file with scraped information about establishments. When referenced in a recall the information about an establishment is inlined into the JSON there, so this is provided simply as a convenience and is not needed for joining data
* [recalls.ndjson](usda/recalls.ndjson) - a ND-JSON file containing information about all the claims that have been scraped from FSIS
* [recalls.csv](usda/recalls.csv) - a CSV representation of the information within recalls.json with the following changes:
  * Newlines are removed in certain strings
  * Array fields are represented in a string joined using ", "
  * Establishment fields are inlined to the top using `establishment_` as a prefix
* [/data/establishments](usda/data/establishments) - HTML snippets / parsed JSON for individual establishments referenced in some recalls
* [/data/recalls](usda/data/recalls) - HTML snippets / parsed JSON of individual recalls. These are organized by subdirectories by year, PHA (for Public Health Alerts) and unknown_year when the year could not be derived

### Local setup

The scrapers are coordinated by using make. To run locally, you can run the following from the root directory

``` sh
make usda
```

This will run tasks to scrape the first 3 pages of recalls and parse any new/changed recalls that it finds. To run the scraper over all USDA pages, run `make usda_full`

### The Magic of make

We can think of the scraper as a data pipeline with the following steps:

1. Scraper runs through the most recent few pages and pulls out HTML snippets for records
2. For any that are new and changed, parse the HTML into a JSON representation
3. If any of the JSON fields have changed, rebuild the big ND-JSON file as well
4. If the ND-JSON file has changed, rebuild the CSV

In essence, instead of thinking of pipelines as a series of conditional actions flowing forward, we can track the upstream dependencies of any point and if and only if those change, take the necessary action downstream. This is the [make](https://www.gnu.org/software/make/manual/make.html) model and it's been powering compilation for decades, so it would makes sense to rebuild data files with it. Spotify's [luigi](https://github.com/spotify/luigi) uses this approach for large data pipelines, but for smaller processes like this, the original make will do.

To see how it works look at the Makefiles in the following places:
* [Makefile](Makefile)
* [usda/Makefile](usda/Makefile)
* [usda/data/recalls/Makefile](usda/data/recalls/Makefile)
* [usda/data/establishments/Makefile](usda/data/establishments/Makefile)

Makefile syntax is a bit obtuse, but here is an example from the recalls Makefile of how some of this works

``` makefile
recalls_html = $(wildcard usda/data/recalls/**/*.html)
recalls_json = $(recalls_html:%.html=%.json)

%.json: %.html
	$(call python,usda/parse_recall.py --src=$< --dest=$@ --establishments=usda/data/establishments)
    
usda/recalls.ndjson: $(recalls_json)
	$(call python,usda/build_recalls_json.py --dir=usda/data/recalls --dest=$@)

usda/recalls.csv: usda/recalls.ndjson
	$(call python,usda/recalls_json_to_csv.py --json=$< --csv=$@)
```
Makefile directives are structured like

``` makefile
target: sources
    actions
```

What the Makefile above does is look for any HTML file in the data/recalls/**/*.html where either there is no corresponding JSON file (or the HTML file has a newer modification time, meaning it has changed). For any file for which that has happened, it runs the `usda/parse_recall.py` script to parse the HTML and save a corresponding JSON file. In turn, the recalls.ndjson would be rebuilt and that would in turn rebuild the recalls.csv
