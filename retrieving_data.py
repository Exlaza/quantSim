import MySQLdb as mdb
import pandas as pd

if __name__ == "__main__":
    db_host = 'localhost'
    db_name = 'securities_master'
    db_pass = 'sec_1234'
    db_user = 'sec_user'

    con = mdb.connect(db_host, db_user, db_pass, db_name)

    #'''or""" is a multiline string banane ka tareeka
    sql = """SELECT dp.price_date, dp.adj_close_price
             FROM daily_price as dp
             INNER JOIN symbol as sym
             ON dp.symbol_id = sym.id
             WHERE sym.ticker = 'GOOG'
             ORDER BY dp.price_date ASC;"""

    #Create a pandas dataframe from the SQL query

    goog = pd.read_sql_query(sql, con = con, index_col = 'price_date')

    print(goog.tail())
