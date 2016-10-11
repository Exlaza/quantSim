"""
The follwoing code will use requests and beautiful
soup4 to scrape wikipedia page containg the list of S&P 500
"""

import datetime
from math import ceil
import bs4
import requests
import MySQLdb as mdb

#This just sets now to the current date, yep that's it
#More details, consider it like This
#first datetime is for the module
#second datetime for that class of the name datetime
#finally we have a class method utcnow
#which return a datetime object something like
#datetime.datetime(2016, 10, 11, 8, 16, 37, 996063)
#doing this for the created_at record
now = datetime.datetime.utcnow()


"""
Two types of most commmonly use HTTP requests
GET and POST
GET Basically gives you all the content in the server
for an example do This
Goto http://testuri.org/sniffer and put https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
Then checkout the content section, that's the whole goddamn html
and requests converts that for you in the form of a
response object from which you vcan extrat information all you like"
"""
response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
