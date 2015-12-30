# http://docs.python-guide.org/en/latest/scenarios/scrape/
from lxml import html
import requests

page = requests.get('http://www.cdf.toronto.edu/usage/usage.html')
tree = html.fromstring(page.content)

names      = tree.xpath('//table/tr[position() > 1]/td[1]/text()')
avail      = tree.xpath('//table/tr[position() > 1]/td[2]/text()')
busy       = tree.xpath('//table/tr[position() > 1]/td[3]/text()')
total      = tree.xpath('//table/tr[position() > 1]/td[4]/text()')
percentage = tree.xpath('//table/tr[position() > 1]/td[5]/text()')
time       = tree.xpath('//table/tr[position() > 1]/td[6]/text()')

print 'Names: ', names
print 'Avail: ', avail
print 'Busy:  ', busy
print 'Total: ', total
print '%:     ', percentage
print 'Time:  ', time
