import urllib.request
import csv
from bs4 import BeautifulSoup

req = urllib.request.Request(url='https://etherscan.io/contractsVerified/1?ps=100',
                             data=None,
                             headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
                                      })

resp = urllib.request.urlopen(req)
respData = resp.read().decode('utf-8')

soup = BeautifulSoup(respData, "lxml")

print("Address, Contract_Name, Compiler, Balance, Tx_count, Date_Verified")

for row in soup.findAll('tbody')[0].findAll('tr'):

    Address = str(row.findAll('a')[0].get_text())
    Contract_name = str(row.findAll('td')[1].get_text())
    Compiler = str(row.findAll('td')[2].get_text())
    Balance = str(row.findAll('td')[3].get_text())
    Tx_count = str(row.findAll('td')[4].get_text())
    Date_verified = str(row.findAll('td')[6].get_text())
    u = Address, Contract_name, Compiler, Balance, Tx_count, Date_verified
    #print(Address, ",", Contract_Name, ",", Compiler, ",", Balance, ",", Tx_count, ",", Date_Verified)
    print(u)
