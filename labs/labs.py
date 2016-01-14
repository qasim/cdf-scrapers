from html.parser import HTMLParser
import datetime
import json
import os
import sys
import time
import urllib.request

class PageParser(HTMLParser):
    """Parser for CDF Lab Machine Usage page."""
    # Flag for whether an element should be parsed
    read_data = False

    # A data row contains 6 cells
    row_cell = 0

    # List of lab rooms/data
    data = []

    # Timestamp
    timestamp = ''

    def handle_starttag(self, tag, attrs):
        # Only read <td> tags
        if (tag == 'td'):
            self.read_data = True

    def handle_data(self, data):
        if (self.read_data):
            if self.row_cell == 0:
                if (data != 'NX'):
                    data = 'BA ' + data

                self.data.append({
                    'name': data
                })

            elif self.row_cell == 1:
                self.data[-1]['available'] = int(data)

            elif self.row_cell == 2:
                self.data[-1]['busy'] = int(data)

            elif self.row_cell == 3:
                self.data[-1]['total'] = int(data)

            elif self.row_cell == 4:
                self.data[-1]['percent'] = float(data)

            elif self.row_cell == 5:
                if (self.timestamp == ''):
                    timestamp = time.strptime(data.strip('\u00a0\\n'), '%a %b %d %H:%M:%S EST %Y')
                    self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S EST', timestamp)

                self.row_cell = -1

            self.row_cell += 1
            self.read_data = False

if __name__ == '__main__':
    html = str(urllib.request.urlopen('http://www.cdf.toronto.edu/usage/usage.html').read())
    parser = PageParser()
    parser.feed(html)

    data = json.dumps({
        'labs'      : parser.data,
        'timestamp' : parser.timestamp
    })

    if len(sys.argv) > 1:
        output = sys.argv[1]

        if not os.path.exists(output):
            os.makedirs(output)

        with open('%s/cdflabs.json' % (output), 'w+') as outfile:
            outfile.write(data)
    else:
        print(data)
