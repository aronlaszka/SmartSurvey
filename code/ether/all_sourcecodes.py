import csv
import urllib.request
from bs4 import BeautifulSoup

with open('etherscanlist2.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Address = row['Address_']
        # print(Address)
        req = urllib.request.Request(url='https://etherscan.io/address/' + str(Address),
                             data=None,
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
                                      })
        with urllib.request.urlopen(req) as response, open('file.txt', 'a') as out_file:
            # making out_file a list so that it can be appended and written into
            out_file = []
            data = response.read()  # a `bytes` object
            # print(data)
            # out_file.write(data)
            soup = BeautifulSoup(data, "lxml")
            for info in soup.findAll('pre', {'class': 'js-sourcecopyarea', 'id': 'editor'}):
                b = info.text.encode('utf-8')
                print(b)
                out_file.append(b)
