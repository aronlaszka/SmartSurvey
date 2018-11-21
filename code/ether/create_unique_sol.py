# SECTION 5 -----------------------------------------------------------------------------------------------
# Looking only for the source code of the contract

from bs4 import BeautifulSoup
import csv
import re
import html

d = {}
# Initializing dictionary d containing {sourcecode string f: x + .sol}
uniques = {}
# Initializing dictionary uniques to store addresses x with unique source codes

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # the first group captures quoted strings (double or single)
    # the second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return ""  # returns empty to remove the comment
        else:  # otherwise, returns the 1st group
            return match.group(1)  # captured quoted-string

    return regex.sub(_replacer, string)

with open(r'etherscanlist4new.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        # print(row[0]) which is Address
        data = [row[0] for row in csv.reader(csvDataFile)]
        # data includes the numbers till n-1 for example [0:2] that displays 1st and second column
        # of 0th/1st row in csv file
        Address = data[0:46188]
        # 46188
        # print(type(Address))
        # print(len(Address))
        for x in Address:
            # print(type(x))
            # print(x)
            # here x is all the 42 bit addresses
            # creating the solidity file
            with open(x + ".htm", 'r', encoding='utf-8') as f_input:
                # open(x + ".sol", 'w', encoding='utf-8') as f_output:
                # here f_input is the.htm file
                # print(f_input)
                soup = BeautifulSoup(f_input, "html.parser")
                for info in soup.findAll('pre', {'class': 'js-sourcecopyarea', 'id': 'editor'}):
                    b = info.text
                    # print(b)
                    c = html.unescape(b)
                    # using html unescape to convert html entities such as "&lt" to "<"
                    u = remove_comments(c)
                    # print(u)
                    h = u.replace(' ', '').replace('\n', '').strip().rstrip().lstrip()
                    # h is the string of the contract without whitespaces and // comments
                    # print(h)
                    if h in d:
                        # print(d)
                        print(f"{x} not unique! first: {d[h]}")
                    else:
                        d[h] = x + ".sol"
                        # print(d[h])
                        # creating the unique solidity files with addressname.sol
                        with open('etherscanlist4new.csv', 'r') as f_read, open(x + ".sol", 'w') as f_write:
                            f_write.write(u)
                        # uniques.append(d[h])
                    uniques[x] = d[h] # assigning values of address dictionary to string dictionary

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


