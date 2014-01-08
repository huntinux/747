#!/usr/bin/python2

import getpage
import requests
import re
from bs4 import BeautifulSoup

baseurl = 'http://www.seatguru.com'
listurl = 'http://www.seatguru.com/airlines/Air_China/information.php'
r = requests.get(listurl)
data = r.text
soup = BeautifulSoup(data)

i = 0
def a_class_standard_pname_td(tag):
	return tag.name == 'a' and tag.parent.name == 'td' and not tag.has_attr('class') 
for a in soup.find_all(a_class_standard_pname_td):
	print baseurl + a['href']
	url = baseurl + a['href']
	getpage.grab_page_info(i, url)
	i = i + 1
	if(i == 10):
		break

#url  = 'http://www.seatguru.com/airlines/Air_China/Air_China_Boeing_747-400.php'
#getpage.grab_page_info(0, url)
