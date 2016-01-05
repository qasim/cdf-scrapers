import json
import time
import datetime
import subprocess

def getData():
    """Returns the print queue jobs in a nicely formatted JSON object."""

    raw_data = subprocess.Popen('lpq -a', shell=True, stdout=subprocess.PIPE).stdout.read()
    data = raw_data.decode('ISO-8859-1').split('\n')

    junk = ['@ps2 \'', 'Rank   Owner/ID', ' printable job', 'no server active',
        'Filter_status: ', ' Status: ', ': pid ']

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
            printer = line.split()[0].split('@')[0]
            parsed[printer] = {
                'name':   printer,
                'jobs':   [],
                'length': 0
            }
            new_printer = True
            continue

        # Actual queued jobs
        if line:
            job_data = line.split()

            job = {
                'raw':   line,
                'rank':  job_data[0],
                'owner': job_data[1],
                'class': job_data[2],
                'job':   job_data[3]
            }
            
            if 'ERROR' in line:
                job['files'] = line[line.index('ERROR'):]
                job['size']  = ''
                job['time']  = ''
            else:
                job['files'] = ' '.join(job_data[4:-2])
                job['size']  = job_data[-2]
                job['time']  = job_data[-1]

            if not job in parsed[printer]['jobs']:
                parsed[printer]['jobs'].append(job)
                parsed[printer]['length'] += 1

    return parsed

if __name__ == '__main__':
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    print(json.dumps({
        'printers':  getData(),
        'timestamp': timestamp
    }))