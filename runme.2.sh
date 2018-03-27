#!/bin/bash
# runme.2.sh
# Author: Moises Marin
# Date: December 3, 2017
# Purpose: launch python scripts to scrape, load Mongo DB and tweet discounts from
# retail sites as per configuration file
#
#

# Get html pages
python3 ./download.py

# Convert to single Json file
python3 ./parse.py

# Reload collection
python3 ./reload.py

# Remove download and parsed folders
python3 ./clean.py

# Three twits - most expensive, least expensive, biggest discount
python3 ./tweet.py


