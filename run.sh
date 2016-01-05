#!/bin/bash

home="/h/u10/g3/00/g3cheunh"
old_dump="$home/public_html/printdata.json"
new_dump="$home/public_html/cdfprinters.json"
labs="$home/public_html/cdflabs.json"

rm -f $old_dump
rm -f $new_dump
rm -f $labs

/local/bin/python3 "$home/cdf-scrapers/printers/printers-deprecated.py" > $old_dump
/local/bin/python3 "$home/cdf-scrapers/printers/printers.py" > $new_dump
/local/bin/python3 "$home/cdf-scrapers/labs/labs.py" > $labs

chmod og+r $old_dump
chmod og+r $new_dump
chmod og+r $labs
