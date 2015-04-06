#!/bin/bash

rm -f /h/u10/g3/00/g3cheunh/public_html/printdata.json
/local/bin/python3 /h/u10/g3/00/g3cheunh/cdf-printdata/lpq.py > /h/u10/g3/00/g3cheunh/public_html/printdata.json
chmod og+r /h/u10/g3/00/g3cheunh/public_html/printdata.json

