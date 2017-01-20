import requests
from bs4 import BeautifulSoup
import urlparse
from pprint import pprint
import re

BASE_URL = "http://www.justdial.com/"


def get_alphanumeric(texts):
    return re.sub(r'\W+', ' ', texts)

def parse_star(soup):
    count = 0
    for i in soup.find_all("span"):
        count = count + int(i['class'][0][1:])
    return float(count)/10


class Just(object):
    """
    Scraped object from just dial
    serialized stored here
    """

    def __init__(self, title, phone, address, address_url, category, established_in, rating_count, star, url):
        self.title = title
        self.phone = phone
        self.address = address
        self.address_url = address_url
        self.category = category
        self.established_in = established_in
        self.rating_count = rating_count
        self.star = star
        self.url = url

    def get_reviews(self):
        # return scrape_reivew(self.url)
        pass


def getfromsearch(query, place):
    """
    - query for the place
    - place is the location eg. hyderbad, city name
    """
    url = "http://www.justdial.com/webmain/autosuggest.php?cases=what&search={}+&city={}&area=&s=1".format(
        query, place)
    # bypass 403 error with headers
    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'  # This is another valid field
    }
    r = requests.get(url, headers=headers)
    pprint(r.json())




def crawlfromsearch(query, place):
    JUSTS= []
    url = "http://www.justdial.com/Ahmedabad/{}-%3Cnear%3E-{}-GPO".format(
        query, place)
    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'  # This is another valid field
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,"lxml")
    s = soup.find("section", class_="rslwrp")
    lists = s.find(
        "ul", class_="rsl col-md-12 padding0").findAll("li", class_="cntanr")
    for l in lists:
        title = l.find("h4").text.strip()
        phone = l.find("p", class_="contact-info").text.strip()
        address = '"'
        try:
            address = l.find(
                "p", class_="address-info adinfoex").find('a')['title']
        except:
            try:
                address = l.find(
                    "p", class_="address-info adinfoex").get_text().strip()
                address = get_alphanumeric(address)
            except:
                pass
        address_url = l.find("p", class_="address-info ").find('a')
        # address_url= None
        category = l.find("span", class_="desk-add jaddt").get_text().strip()
        category = get_alphanumeric(category)
        established_in = l.find("ul", class_="est-info ipadabove")
        star = l.find("span", class_="star_m")

        if star == None:
            star = 0
        try:
            star = parse_star(star)
        except:
            pass
        rating_count = l.find("span", class_="rt_count").get_text()
        rating_count = get_alphanumeric(rating_count)
        established_in = l.find("span", class_="year").get_text()
        url = l.find("span", class_="jcn").find("a")['href']
        J = Just(title=title,phone=phone,address=address,address_url=address_url,category=category,established_in=established_in,rating_count=rating_count,star=star,url=url)
        JUSTS.append(J)

    return JUSTS

for i in crawlfromsearch("hello","hyderabad"):
    pprint (i.__dict__)