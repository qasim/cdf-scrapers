import argparse
import os
import sys

class Scraper:
    """Scraper superclass."""

    def __init__(self):
        argparser = argparse.ArgumentParser(description='Scraper for CDF lab data.')
        argparser.add_argument('-o', '--output', help='The output path. Defaults to current directory.', required=False)
        argparser.add_argument('-f', '--filename', help='The output filename. Defaults to "cdflabs.json".', required=False)

        args = argparser.parse_args()
        output = '.'
        filename = 'cdflabs.json'

        if args.output:
            if not os.path.exists(args.output):
                os.makedirs(args.output)

            output = args.output

        if args.filename:
            filename = args.filename

        if args.output or args.filename:
            with open('%s/%s' % (output, filename), 'w+') as outfile:
                outfile.write(data)
        else:
            print(data)
