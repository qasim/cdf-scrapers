import json
import time
import datetime
import subprocess

def getData(printer):
    """Return the data from calling lpq with the specified printer."""
    cmd = 'lpq -P' + printer
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return(data.decode('utf-8'))

def parseData(list):
    """Returns the list without the header lines."""
    return list[0:]

if __name__ == '__main__':
    # Gets all the data
    p2210a = getData('p2210a').split('\n')
    p2210b = getData('p2210b').split('\n')
    p3185a = getData('p3185a').split('\n')

    data = {}

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    data['timestamp'] = st
    
    data['2210a'] = parseData(p2210a)
    data['2210b'] = parseData(p2210b)
    data['3185a'] = parseData(p3185a)

    json_data = json.dumps(data)

    print(json_data)

