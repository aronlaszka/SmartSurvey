    with open('etherscan1.csv', 'r') as file_handle:
        lines = file_handle.readlines()

    with open('etherscanlist1.csv', 'w') as file_handler:
        lines = filter(lambda x: x.strip(), lines)
        file_handler.writelines(lines)

    rows = ['Address', 'Contract Name', 'Compiler', 'Balance', 'Tx count', 'Date verified']
    with open('etherscanlist1.csv', 'r') as old_file, open('etherscanlist2.csv', 'w') as new_file:
        writer = csv.DictWriter(new_file, delimiter=' ', lineterminator='\n',
                                fieldnames=['Address_', 'Contract_Name', 'Compiler_', 'Balance_', 'Tx_count',
                                            'Date_verified'])
        writer.writeheader()
        for line in old_file:
            if not any(row in line for row in rows):
                new_file.write(line)
