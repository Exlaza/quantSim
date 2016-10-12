"""
The following code will use requests and beautiful
soup4 to scrape wikipedia page containg the list of S&P 500
"""

import datetime
from math import ceil
import bs4
import requests
import MySQLdb as mdb

def obtain_parse_wiki_snp500():

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
    response object from which you can extract information all you like"
    """
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    """
    Okay, the waY BeautifulSoup works is insanely intuitive
    Official documentation is really good....works somewhat like a dicitonary but it is exatly not a dictionary
    """
    soup = bs4.BeautifulSoup(response.text)

    """
    Okay, Now If you loook at the source code that i supplied to soup object int he
    for of response.text, then you would realize that in the first
    "table" tag I have different "tr" tage representing various coloumn
    And the liine below would give me a list of all the tr tags exclusing the first(
    hence the [1:]) and you can just select any other tag under them by doing select again
    Think intuitively
    """
    symbolsList = soup.select("table")[0].select('tr')[1:]

    symbols = []
    for symbol in symbolsList:
        tds = symbol.select('td')
        symbols.append((tds[0].select('a')[0].text, 'stock', tds[1].select('a')[0].text, tds[3].text, 'USD', now, now))
    return symbols

def insert_snp500_symbols(symbols):
    db_host = 'localhost'
    db_user = 'sec_user'
    db_name = 'securities_master'
    db_pass = 'sec_1234'

    con = mdb.connect(host = db_host, user = db_user, passwd = db_pass, db = db_name)

    column_string = "ticker, instrument, name, sector, currency, created_date, last_updated_date"
    insert_string = ("%s, " * 7)[:-2]
    final_string = 'INSERT INTO symbol (%s) VALUES (%s)' % (column_string, insert_string)
    with con:
        cur = con.cursor()

        cur.executemany(final_string, symbols)

if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    insert_snp500_symbols(symbols)
    print("%s symbols were successfully added" % (len(symbols)))
