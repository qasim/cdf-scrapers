#!/bin/bash

home="/h/u10/g3/00/g3cheunh"
old_dump="$home/public_html/printdata.json"
new_dump="$home/public_html/cdfprinters.json"

rm -f $old_dump
rm -f $new_dump

/local/bin/python3 "$home/cdf-scrapers/printers/lpq-old.py" > $old_dump
/local/bin/python3 "$home/cdf-scrapers/printers/lpq.py" > $new_dump

chmod og+r $old_dump
chmod og+r $new_dump
