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
