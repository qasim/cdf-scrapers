#!/bin/bash

home="/h/u10/g3/00/g3cheunh"
labs="$home/public_html/cdflabs.json"

rm -f $labs

/local/bin/python3 "$home/cdf-scrapers/labs/labs.py" > $labs

chmod og+r $labs
