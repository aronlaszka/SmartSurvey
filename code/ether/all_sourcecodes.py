# SECTION 4-------------------------------------------------------------------------------------
# Downloading individual html pages of the contract source code

import urllib.request
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep
import re
import pyparsing

with open('etherscanlist4new.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Address = row['Address']
        # print(Address)
        req = urllib.request.Request(url='https://etherscan.io/address/' + str(Address),
                             data=None,
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
                                      })
        # Specify user agent to gain access
        sleep(randint(8, 15))
        # sleep used to slow down the url request
        response = urllib.request.urlopen(req)
        responseData = response.read()
        # removed decode statement so that data is in bytes
        print(responseData)

        with open(str(Address) + ".htm", 'wb') as f_out:
            f_out.write(bytes(responseData))

# SECTION 5 -----------------------------------------------------------------------------------------------
# Looking only for the source code of the contract

d = {}

with open(r'etherscanlist4new.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        # print(row[0]) which is Address
        data = [row[0] for row in csv.reader(csvDataFile)]
        # data includes the numbers till n-1 for example [0:2] that displays 1st and second column
        # of 0th/1st row in csv file
        Address = data[0:6] # 46188]
        for x in Address:
            # print(x) here x is all the 42 bit addresses
            # creating the solidity file
            with open(x + ".htm", 'r', encoding='utf-8') as f_input: # open(x + ".sol", 'w', encoding='utf-8') as f_output:
                # print(f_input)
                soup = BeautifulSoup(f_input, "html.parser")
                for info in soup.findAll('pre', {'class': 'js-sourcecopyarea', 'id': 'editor'}):
                    b = info.text
                    # # print(b)
                    # clean white space and tabs
                    b = b.replace(' ', '')
                    comment = pyparsing.nestedExpr("/*", "*/").suppress()
                    c = comment.transformString(b)
                    # print(c)
                    c = c.split()
                    e = [x for x in c if not '//' in x]
                    f = ''.join(e)
                    f = f.replace(' ', '').replace('\n', '').strip().rstrip().lstrip()
                    # f is the string of the contract without whitespaces and comments
                    # print(f)

                    # d[f] = 1

                    # print(d)
                    if f in d:
                        # print(d)
                        print(f"{x} not unique!  first: {d[f]}")
                    else:
                        d[f] = x + ".sol"
                        # creating the unique solidity files with addressname.sol
                        with open('etherscanlist4new.csv', 'r') as f_read, open(x + ".sol", 'w') as f_write:
                            f_write.write(f)

                        with open('etherscanlist4new.csv', 'r') as f_read1, open('etherscanlist5new.csv', 'w') as f_write1:
                            rows = []
                            for row_all in f_read1:
                                if row_all in rows:
                                    continue
                                else:
                                    f_write1.write(row_all)
                                    rows.append(row_all)
                        f_read1.close()
                        f_write1.close()

                        with open('etherscanlist5new.csv', 'w') as f_write2:
                            row[6] = d[f]
                            rows.append(row[6])
