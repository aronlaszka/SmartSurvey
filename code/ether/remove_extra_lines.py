# SECTION 3-------------------------------------------------------------------------------------
import urllib.request
from bs4 import BeautifulSoup
import csv
from random import randint
from time import sleep

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
