from lxml import html
import requests
import csv,os,time
joiner=' , '
def modifyEntry(entry):
    if len(entry)==0:
        entry.append('')
def createTree(link):
    page = requests.get(link)
    tree = html.fromstring(page.text)
    return tree

def extractLinkWithTree(tree,xpath):
    temp = tree.xpath(xpath)
    #print temp
    return temp

def extractLink(link,xpath):
    return extractLinkWithTree(createTree(link),xpath)

def uniq(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output


mainPageLink=raw_input("Enter a valid link of justdial page: ")
dir_path=raw_input("Enter a folder name: ")
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
print "Extracting data:\nPlease wait...\n"
pageLink=[mainPageLink]
pageLink+=extractLink(mainPageLink,'//*[@class="jpag"]/a/@href')

for x in pageLink:
    pageLink+=extractLink(x,'//*[@class="jpag"]/a/@href')
    print pageLink
    pageLink=uniq(pageLink)


print "\n\n\nPage List Prepared. Writing to file page_list.csv\n"

with open(dir_path+'/file_list.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for data in pageLink:
        print data
        spamwriter.writerow([data])
    

print "Writing to file page_list.csv completed.\n"
print "Analysing  pages..\n"
print "Extracting entries"

with open(dir_path+'/entries.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
    for page in pageLink:

        for LinkInPage in extractLink(page,'//p[@class="jcnwrp"]/span/a/@href'):
            while (1):
                tree=createTree(LinkInPage)
                name=extractLinkWithTree(tree,"//*[@class='fn']/text()")
                address=extractLinkWithTree(tree,"//span[@class='jaddt'][2]/text() ")
                tel=extractLinkWithTree(tree,"//*[@class='tel']//text()")
                tel=uniq(tel)
                website=extractLinkWithTree(tree,"//*[@class='wsurl']/a/@href")
                website=uniq(website)
                modifyEntry(website)
                modifyEntry(address)
                modifyEntry(tel)
                modifyEntry(name)
                row= [(name[0].strip()).encode('ascii','ignore')]+[address[0].strip().encode('ascii','ignore')]+[((joiner.join(tel)).strip()).encode('ascii', 'ignore')]+[website[0].strip().encode('ascii','ignore')]
                #row=row1.encode('ascii','ignore') 
                if (row!=['','','','']):
                    #print (row!=['','','',''])
                    break
                
                time.sleep(1)
            spamwriter.writerow(row)        
            print row

print "Fetching entries finished"