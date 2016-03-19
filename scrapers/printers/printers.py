import argparse
import datetime
import json
import os
import subprocess
import sys
import time

def getData():
    """Returns the print queue jobs in a nicely formatted JSON object."""

    raw_data = subprocess.Popen('lpq -a', shell=True, stdout=subprocess.PIPE).stdout.read()
    data = raw_data.decode('ISO-8859-1').split('\n')

    junk = ['@ps2 \'', 'Rank   Owner/ID', ' printable job', 'no server active',
        'Filter_status: ', ' Status: ', ': pid ']

    parsed = []
    new_printer = False

    for line in data:
        # New printer section: get description
        if new_printer:
            if '@ps2' in line:
                parsed[-1]['description'] = line.split('@ps2 ')[1].replace("'", "")
            else:
                parsed[-1]['description'] = line
            new_printer = False
            continue

        # Skip lines we don't care about
        if any(x in line for x in junk):
            continue

        # First line of section for a printer
        if '@printsrv)' in line:
            printer = line.split()[0].split('@')[0]
            parsed.append({
                'name'   : printer,
                'jobs'   : [],
                'length' : 0
            })
            new_printer = True
            continue

        # Actual queued jobs
        if line:
            job_data = line.split()

            job = {
                'raw'   : line,
                'rank'  : job_data[0],
                'owner' : job_data[1],
                'class' : job_data[2],
                'job'   : job_data[3]
            }

            if 'ERROR' in line:
                job['files'] = line[line.index('ERROR'):]
                job['size']  = ''
                job['time']  = ''
            else:
                job['files'] = ' '.join(job_data[4:-2])
                job['size']  = job_data[-2]
                job['time']  = job_data[-1]

            if not job in parsed[-1]['jobs']:
                parsed[-1]['jobs'].append(job)
                parsed[-1]['length'] += 1

    return parsed

if __name__ == '__main__':
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S EST')

    data = json.dumps({
        'printers'  : getData(),
        'timestamp' : timestamp
    })

    argparser = argparse.ArgumentParser(description='Scraper for CDF printer queue data.')
    argparser.add_argument('-o', '--output', help='The output path. Defaults to current directory.', required=False)
    argparser.add_argument('-f', '--filename', help='The output filename. Defaults to "cdfprinters.json".', required=False)

    args = argparser.parse_args()
    output = '.'
    filename = 'cdfprinters.json'

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
