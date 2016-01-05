from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
    def handle_data(self, data):
        print("Encountered some data  :", data)

html = str(urllib.request.urlopen('http://www.cdf.toronto.edu/usage/usage.html').read())
parser = MyHTMLParser()
parser.feed(html)
