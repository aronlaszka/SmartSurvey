# RUN SECTIONS IN ORDER 1, 2-3, 4, 5
# SECTION 1 -----------------------------------------------------------------------------------------------
import urllib.request
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep

maxpage = 461
# looping through all 462 pages and reading
for page in range(1, maxpage + 1):
    # print(page)
    req = urllib.request.Request(url='https://etherscan.io/contractsVerified/' + str(page) + '?ps=100',
                                 data=None,
                                 headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
                                         })
    # Specify user agent to gain access
    sleep(randint(8, 15))
    # sleep used to slow down the url request
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    # removed decode statement so that data is in bytes
    print(respData)

    with open(str(page) + ".htm", 'wb') as f_out:
        f_out.write(bytes(respData))

# ------------------------------------------------------------------------------
# SECTION 2 -----------------------------------------------------------------------------------------------

for page in range(1, 463):
    with open(str(page) + ".htm", 'r', encoding='utf-8') as fin:

        soup = BeautifulSoup(fin, "html.parser")
        rows = []

# contract list html page has only one 'tbody' class so find that
        for row in soup.findAll('tbody')[0].findAll('tr'):
            # extract table section in verified contracts page
            Address = (row.findAll('a')[0].get_text())
            Contract_name = (row.findAll('td')[1].get_text())
            Compiler = (row.findAll('td')[2].get_text())
            Balance = (row.findAll('td')[3].get_text()).replace(',', '').replace('Ether', '').replace('-', '0')
            # print(Balancece)
            # print(type(Balance)) is string
            if "wei" in Balance:
                # cannot use Balance.find("wei" as it works on all lines)
                Balance = Balance.replace('wei', '')
                # print(Balance)
                Balance = float(Balance)/1000000000000000000
                # must be converted back to string as cannot write to csv file if Balance is float
                Balance = str(Balance)
            # print(Balance)
            # replace ether and wei to get only numbers, replace , with blank space so numbers don't shift rows in excel
            Tx_count = (row.findAll('td')[4].get_text())
            Date_verified = (row.findAll('td')[6].get_text())
            u = Address, Contract_name, Compiler, Balance, Tx_count, Date_verified
            # print(Address, ",", Contract_Name, ",", Compiler, ",", Balance, ",", Tx_count, ",", Date_Verified)
            print(u)
            rows.append(u)

# now write all the table columns to a csv file
        with open('etherscan1new.csv', 'a') as csvfile:
            fieldnames = ['Address', 'Contract Name', 'Compiler', 'Balance', 'Tx count', 'Date verified']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                csvfile.write(",".join(row))
                csvfile.write("\n")

# SECTION 3-------------------------------------------------------------------------------------
# Remove blank lines in between data
with open('etherscan1new.csv', 'r') as file_handle:
    lines = file_handle.readlines()
with open('etherscanlist1new.csv', 'w') as file_handler:
    lines = filter(lambda x: x.strip(), lines)
    file_handler.writelines(lines)

# Remove extra header rows starting with Address as they printed for every contract page
rows = ['Address', 'Contract Name', 'Compiler', 'Balance', 'Tx count', 'Date verified']
with open('etherscanlist1new.csv', 'r') as inp, open('etherscanlist2new.csv', 'w', newline='') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0] != "Address":
            writer.writerow(row)

# Add one final header row to the final list
with open('etherscanlist2new.csv', 'r') as inp1, open('etherscanlist3new.csv', 'w', newline='') as out1:
    fieldnames = ['Address', 'Contract Name', 'Compiler', 'Balance', 'Tx count', 'Date verified']
    writer = csv.DictWriter(out1, fieldnames=fieldnames)
    writer.writeheader()
    lines = inp1.readlines()
    out1.writelines(lines)

# Below section to remove contracts that were repeated while downloading
# so that there are exactly 46187 as in screen-shot
with open('etherscanlist3new.csv', 'r') as inFile, open('etherscanlist4new.csv', 'w') as outFile:
    listLines = []
    for line in inFile:
        if line in listLines:
            continue
        else:
            outFile.write(line)
            listLines.append(line)
outFile.close()
inFile.close()

# SECTION 4-------------------------------------------------------------------------------------
# Downloading individual html pages of the contract source code

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

from bs4 import BeautifulSoup
import csv
import re
import pyparsing

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
                        # with open('etherscanlist4new.csv', 'r') as f_read, open(x + ".sol", 'w') as f_write:
                        #     f_write.write(f)

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
                            
                        # with open('etherscanlist5new.csv', 'r') as fin_read, open('etherscanlist5new.csv', 'w') as fout_write:
                        #     reader = csv.reader(fin_read)
                        #     writer = csv.writer(fout_write)
                        #     for row2 in reader:
                        #         row[6] = d[f]
                        #         writer.writerow(row2)
                        #     fin_read.close()
                        #     fout_write.close()

                        # if f in d:
                        #     # print(f)
                        #     # print(len(d))
                        #     print(f"{x} not unique! first: {d[f]}")
                        #     # print("yes")
                        # else:
                        #     # write b in to file
                        #     d[f] = x + ".sol"
                        #     print(d[f])
                        #     # f_output.write(f)
