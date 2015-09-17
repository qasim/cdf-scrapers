import json
import time
import datetime
import subprocess

def getData(printer):
    """Return the data from calling lpq with the specified printer as a list."""
    cmd = 'lpq -P' + printer
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return(data.decode('ISO-8859-1').split('\n'))

def parseData(data):
    """Returns the print queue jobs in a nicely formatted list of JSON objects."""
    parsed = []
    queued = False

    for line in data:
        # Skip all the header lines
        if 'Rank   Owner/ID' in line:
            queued = True
            continue

        # Actual queued jobs
        if queued and line:
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

            parsed.append(job)

    return parsed

if __name__ == '__main__':
    # Gets all the data
    p2210a = getData('p2210a')
    p2210b = getData('p2210b')
    p3185a = getData('p3185a')

    # Put data and timestamp in JSON to print to stdout
    data = {}

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    data['timestamp'] = st
    data['2210a'] = parseData(p2210a)
    data['2210b'] = parseData(p2210b)
    data['3185a'] = parseData(p3185a)

    print(json.dumps(data))
