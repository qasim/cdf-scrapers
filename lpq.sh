#!/bin/bash

home="/h/u10/g3/00/g3cheunh"

rm -f "$home/public_html/printdata.json"
rm -f "$home/public_html/cdfprinters.json"

/local/bin/python3 "$home/cdf-printdata/lpq.py" > "$home/public_html/printdata.json"
/local/bin/python3 "$home/cdf-printdata/lpqa.py" > "$home/public_html/cdfprinters.json"

chmod og+r "$home/public_html/printdata.json"
chmod og+r "$home/public_html/cdfprinters.json"

