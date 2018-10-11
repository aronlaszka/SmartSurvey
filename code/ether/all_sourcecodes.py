import csv
import urllib.request

# waiting for list of contracts to be updated so that this code can be checked
with open('etherscanlist3.csv') as csvfile:
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

            # soup = BeautifulSoup(data, "lxml")
            # for info in soup.findAll('pre', {'class': 'js-sourcecopyarea', 'id': 'editor'}):
                # b = info.text.encode('utf-8')
                # print(b)
                # out_file.append(b)

