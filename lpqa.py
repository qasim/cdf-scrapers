import json
import time
import datetime
import subprocess

def getData():
    """Returns the print queue jobs in a nicely formatted list of JSON objects."""

    raw_data = subprocess.Popen('lpq -a', shell=True, stdout=subprocess.PIPE).stdout.read()
    data = raw_data.decode('ISO-8859-1').split('\n')

    junk = ['@ps2 \'', 'Rank   Owner/ID', 'no printable jobs in queue', 'no server active', 'Filter_status: ']

    parsed = {}
    printer = ''
    new_printer = False

    for line in data:
        # New printer section: get description
        if new_printer:
            parsed[printer]['description'] = line.split('@ps2 ')[1]
            new_printer = False
            continue

        # Skip lines we don't care about
        if any(x in line for x in junk):
            continue

        # First line of section for a printer
        if '@printsrv)' in line:
            header_data = line.split()
            printer = header_data[0].split('@')[0]
            parsed[printer] = {}
            parsed[printer]['jobs'] = []
            new_printer = True
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

            parsed[printer]['jobs'].append(job)

    return parsed

if __name__ == '__main__':
    # Gets all the data
    data = getData()

    # Add timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    data['timestamp'] = st

    print(json.dumps(data))
