# SECTION 2-------------------------------------------------------------------------------------
# Remove blank lines
import csv

with open('etherscan1new.csv', 'r') as file_handle:
    lines = file_handle.readlines()
with open('etherscanlist1new.csv', 'w') as file_handler:
    lines = filter(lambda x: x.strip(), lines)
    file_handler.writelines(lines)

# Remove extra header rows starting with Address
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
