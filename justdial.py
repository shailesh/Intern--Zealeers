try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
#--------------------------------------------------------------------------------

import contentUrlJustDial  
from bs4 import BeautifulSoup

import csv
#--------------------------------------------------------------------------------
contentUrlJustDial.getUrlList(3000)
#--------------------------------------------------------------------------------
fileOut = open('Address_MumbaiShops.txt', 'w')
#--------------------------------------------------------------------------------
with open('Mumbai.csv', 'w') as fp:
	csv_writer = csv.writer(fp)
	csv_writer.writerow(('Store Name', 'Contact No', 'Place'))
	fi = open('Mumbai.txt', 'r')
	for line in fi:
		try:
			content = urlopen(line).read()
			soup = BeautifulSoup(content, "html.parser")
			detail = list()
			# soup.find('span', { "class" : "fn" })
			# print("Store Name: "+ soup.find_all('span', { "class" : "fn" })[0].get_text().encode('utf-8'))
			detail.append(soup.find_all('span', { "class" : "fn" })[0].get_text().encode('utf-8'))
			contact_number = ''
			for tele_no in soup.find_all('a', { "class" : "tel" }):
				contact_number = contact_number + tele_no.get_text().encode('utf-8') +', '
			# print("Contact No: " +contact_number)
			detail.append(contact_number)
			# print("Address: " + soup.find("span", {"id": "fulladdress"}).getText().encode('utf-8'))
			addr = soup.find_all('span', {"class" : "adrstxtr" })[0].get_text().encode('utf-8')
			# detail.append(addr)
			fileOut.write( addr + "\n")
			detail.append('Thane')

			csv_writer.writerow(tuple(detail))
		except Exception as e:
			print e.message
			print('Alok')
	fi.close()