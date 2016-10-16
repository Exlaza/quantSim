import requests
import MySQLdb as mdb
import datetime

db_host = 'localhost'
db_name ='securities_master'
db_pass = 'sec_1234'
db_user = 'sec_user'

con = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():

    with con:
        cur = con.cursor()
        cur.execute("SELECT id,ticker FROM symbol where id <=505")
        data = cur.fetchall()
        #return [(d[0],d[1] for d in data)]
        #I think the above line is converting tuple of tuple
        #which is the reuslst of fetchall()
        #into a list of tuples
        appendedData = []
        for d in data:
            appendedData.append((d[0],d[1]))
        return appendedData

def get_daily_historic_data_from_yahoo(ticker, start_date = (2010,1,1), end_date = datetime.date.today().timetuple()[0:3] ):
#http://ichart.finance.yahoo.com/table.csv?s=WU&a=01&b=19&c=2010&d=01&e=19&f=2014&g=d
#wu is the ticker,
#if you want the second month then you would have to put(2-1) as the input
#fROM DATE &a=01&b=18&c=2010
#To date &d=01&e=19&f=2010

    yahoo_url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d" % (ticker, start_date[1]-1, start_date[2], start_date[0], end_date[1]-1, end_date[2], end_date[0])

    try:
        response = requests.get(yahoo_url)
        yf_data = response.text.split()[2:-1] #Return a list of all the sentences in different lines
        prices = []
        #print(yf_data)
        for y in yf_data:
            p = y.strip().split(',')
            print(p[0])
            prices.append((datetime.datetime.strptime(p[0], '%Y-%m-%d'), p[1], p[2], p[3], p[4], p[5], p[6]))
    except Exception as e:
        print("Could not Download pricing data from Yahoo : %s" % e)
    return prices

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    now = datetime.datetime.utcnow()

    refined_daily_data = []
    for d in daily_data:
        refined_daily_data.append((data_vendor_id, symbol_id, d[0], now, now, d[1], d[2], d[3], d[4], d[5], d[6]))

    column_string = "data_vendor_id, symbol_id, price_date, created_date, last_updated_date, open_price, high_price, low_price, close_price, adj_close_price, volume"
    insert_string = ("%s, " * 11)[:-2]#Just removing the space
    final_string = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_string, insert_string)

    cur = con.cursor()
    with con:
        cur.executemany(final_string, refined_daily_data)

if __name__ == "__main__":
    appendedData = obtain_list_of_db_tickers()
    lentickers = len(appendedData)
    for i, d in enumerate(appendedData):
        print(("Adding price information for %s: %s out of %s") % (d[1], i+1, lentickers))
        daily_data = get_daily_historic_data_from_yahoo(d[1])
        insert_daily_data_into_db('1', d[0], daily_data)
    print("Successfully added Yahoo finance pricing data to Database")
