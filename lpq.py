import json
import time
import datetime
import subprocess

def getData():
    """Return the data from calling lpq -a as a list."""
    cmd = 'lpq -a'
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return(data.decode('ISO-8859-1').split('\n'))

def parseData(data):
    """Returns the print queue jobs in a nicely formatted list of JSON objects."""
    parsed = {}
    printer = ''

    for line in data:
        # First line of section for a printer
        if '@printsrv)' in line:
            header_data = line.split()
            printer = header_data[0]
            parsed[printer] = []
            continue

        if '@wolf ' in line or '@ps2 \'' in line:
            continue

        if 'Rank   Owner/ID' in line:
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

            parsed[printer].append(job)

    return parsed

if __name__ == '__main__':
    # Gets all the data
    raw_data = getData()

    # Put data and timestamp in JSON to print to stdout
    data = parseData(raw_data)

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    data['timestamp'] = st

    print(json.dumps(data))
