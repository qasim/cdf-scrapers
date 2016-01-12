import datetime
import json
import os
import subprocess
import sys
import time

# THIS FILE IS DEPRECATED
# This is used to generate the JSON file used in older versions of the CDF Labs Android app.
# It is only updated to deal with bugs.

def getData():
    """Returns the print queue jobs in a nicely formatted list of JSON objects."""

    raw_data = subprocess.Popen('lpq -a', shell=True, stdout=subprocess.PIPE).stdout.read()
    data = raw_data.decode('ISO-8859-1').split('\n')

    junk = ['@ps2 \'', 'Rank   Owner/ID', ' printable job', 'no server active',
        'Filter_status: ', ' Status: ', ': pid ']

    parsed = {}
    printer = ''

    for line in data:
        # Skip lines we don't care about
        if any(x in line for x in junk):
            continue

        # First line of section for a printer
        if '@printsrv)' in line:
            header_data = line.split()
            printer = header_data[0].split('@')[0][1:]
            parsed[printer] = []
            continue

        # Actual queued jobs
        if line:
            job_data = line.split()

            job = {}
            job['raw']   = line
            job['rank']  = job_data[0]
            job['owner'] = job_data[1]
            job['class'] = job_data[2]
            job['job']   = job_data[3]

            if 'ERROR' in line:
                job['files'] = line[line.index('ERROR'):]
                job['size']  = ''
                job['time']  = ''
            else:
                job['files'] = ' '.join(job_data[4:-2])
                job['size']  = job_data[-2]
                job['time']  = job_data[-1]

            if not job in parsed[printer]:
                parsed[printer].append(job)

    return parsed

if __name__ == '__main__':
    # Gets all the data
    data = getData()

    # Add timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + ' EST'

    data['timestamp'] = st

    output = json.dumps(data)

    if len(sys.argv) > 1:
        output_path = sys.argv[1]

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        with open('%s/printdata.json' % (output_path), 'w+') as outfile:
            outfile.write(output)
    else:
        print(output)
