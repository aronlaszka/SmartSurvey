# SECTION 5 -----------------------------------------------------------------------------------------------
# Looking only for the source code of the contract

from bs4 import BeautifulSoup
import csv
import re
import pyparsing

d = {}
# Initializing dictionary d containing {sourcecode string f: x + .sol}
uniques = {}
# Initializing dictionary uniques to store addresses x with unique source codes


with open(r'etherscanlist4new.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        # print(row[0]) which is Address
        data = [row[0] for row in csv.reader(csvDataFile)]
        # data includes the numbers till n-1 for example [0:2] that displays 1st and second column
        # of 0th/1st row in csv file
        Address = data[0:46188] # 46188]
        # print(type(Address))
        # print(len(Address))
        for x in Address:
            # print(type(x))
            # print(x) here x is all the 42 bit addresses
            # creating the solidity file
            with open(x + ".htm", 'r', encoding='utf-8') as f_input:
                # open(x + ".sol", 'w', encoding='utf-8') as f_output:
                # print(f_input)
                soup = BeautifulSoup(f_input, "html.parser")
                for info in soup.findAll('pre', {'class': 'js-sourcecopyarea', 'id': 'editor'}):
                    b = info.text
                    # # print(b)
                    # clean white space and tabs
                    b = b.replace(' ', '')
                    # comment = pyparsing.nestedExpr("/*", "*/").suppress()
                    # c = comment.transformString(b)
                    # print(c)
                    c = b.split()
                    e = [x for x in c if not '//' in x]
                    f = ''.join(e)
                    f = f.replace(' ', '').replace('\n', '').strip().rstrip().lstrip()
                    # f is the string of the contract without whitespaces and comments
                    # print(f)
                    # print(d)
                    if f in d:
                        # print(d)
                        print(f"{x} not unique! first: {d[f]}")
                    else:
                        d[f] = x + ".sol"
                        # print(d[f])
                        # creating the unique solidity files with addressname.sol
                        with open('etherscanlist4new.csv', 'r') as f_read, open(x + ".sol", 'w') as f_write:
                            f_write.write(f)
                        # uniques.append(d[f])
                    uniques[x] = d[f] # assigning values of address dictionary to string dictionary

with open('etherscanlist4new.csv', 'r') as csvinput, open('etherscanlist5new.csv',  'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)

    row = next(reader) # selecting row next to last row
    row.append('Unique solidity files') # header
    # all.append(row)
    writer.writerow(row)

    print(row)

    for row in reader:
        row.append(uniques[row[0]] if row[0] in uniques else '')
        # appending unique files from addresses contracts in row 0
        # all.append(row)
        writer.writerow(row)

    writer.writerow(row)


