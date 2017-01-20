from bs4 import BeautifulSoup
import urllib2
import csv
import time

rawcsvfilename = str(raw_input("Enter the name of the file which contains the city and area : "))  # This is the file which will have the city and the area name.
rawcsvfileopen = open(rawcsvfilename, "rb")
rawcsvdata = csv.reader(rawcsvfileopen, delimiter = ',')  # reading the csv file

cities = []
areas = []

for data in rawcsvdata:
	rawdata = str(data).replace("'", '').replace("[", "").replace("]", "").split(",")
	cities.append(str(rawdata[0]).strip())
	areas.append(str(rawdata[1]).strip())

keyword = str(raw_input("Please enter the keyword for search : "))  # Get the keyword which needs to be searched

limit = len(cities)
counter = 0

outputcsvname = open("outputmobile.csv", "a")
outputcsvm = csv.writer(outputcsvname, delimiter=",")
outputcsvm.writerow(["Search Date & Time", time.strftime("%d/%m/%Y %H:%M:%S")])
outputcsvm.writerow(["City", "Area", "Number", "Keyword"])

outputcsvname = open("outputlandline.csv", "a")
outputcsvl = csv.writer(outputcsvname, delimiter=",")
outputcsvl.writerow(["Search Date & Time", time.strftime("%d/%m/%Y %H:%M:%S")])
outputcsvl.writerow(["City", "Area", "Number", "Keyword"])

stdprefix = str(raw_input("Please enter the prefix provience with country code (eg. 9122) : "))
while True:
	url = "http://www.justdial.com\/%s/%s-<near>-%s" % (cities[counter], keyword, areas[counter]) # this line contains the base url
	counter += 1
	content = urllib2.urlopen(url).read()
	
	soup = BeautifulSoup(content)  # get the content from the website

	try:  # this try is used to find the numbers
		for link in soup.find_all('a'):  # find all the tags with a
			if "tel:+" in link.get('href'):  # get the href tag which contains the tel
				newnum = str(link.get('href')).replace("tel:+", "")
				if stdprefix == newnum[:4]:
					outputcsvl.writerow([cities[counter], areas[counter], newnum, keyword])  # write the number to the csv
				else:
					outputcsvm.writerow([cities[counter], areas[counter], newnum, keyword])  # write the number to the csv
	except:
		print "In process"

	if len(cities) == counter:
		print "Done!"
		break
	# try:  # this try is used to find names, not working properly
	# 	for link in soup.find_all(onclick="_ct('clntnm','lspg');"):
	# 		print "a"
	# 		#print(link.get('title'))
	# except:
	# 	print ""