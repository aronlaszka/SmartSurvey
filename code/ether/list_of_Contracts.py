import urllib.request
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep

page = 449
for counter in range(1, page):
    page = page - 1
    # print(page)
    req = urllib.request.Request(url='https://etherscan.io/contractsVerified/' + str(page) + '?ps=100',
                                 data=None,
                                 headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
                                         })
    sleep(randint(8, 15))
    resp = urllib.request.urlopen(req)
    respData = resp.read().decode('utf-8')
    # print(respData)
    soup = BeautifulSoup(respData, "lxml")
    # print("Address, Contract_Name, Compiler, Balance, Tx_count, Date_Verified")

    rows = []

    for row in soup.findAll('tbody')[0].findAll('tr'):
        Address = (row.findAll('a')[0].get_text())
        Contract_name = (row.findAll('td')[1].get_text())
        Compiler = (row.findAll('td')[2].get_text())
        Balance = (row.findAll('td')[3].get_text())
        Tx_count = (row.findAll('td')[4].get_text())
        Date_verified = (row.findAll('td')[6].get_text())
        u = Address, Contract_name, Compiler, Balance, Tx_count, Date_verified
        # print(Address, ",", Contract_Name, ",", Compiler, ",", Balance, ",", Tx_count, ",", Date_Verified)
        print(u)
        rows.append(u)

    with open('etherscan1.csv', 'a') as csvfile:
        fieldnames = ['Address', 'Contract Name', 'Compiler', 'Balance', 'Tx count', 'Date verified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            csvfile.write(",".join(row))
            csvfile.write("\r\n")
