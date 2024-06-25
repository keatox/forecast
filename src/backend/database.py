from dotenv import load_dotenv, find_dotenv
import numpy as np
import psycopg2
import os

class Database:
    def __init__(self):
        self.stock = None
        self.__tickers = np.vstack((np.loadtxt('res/nasdaq.txt',skiprows=1,dtype=str,delimiter='\t'),
                                    np.loadtxt('res/nyse.txt',skiprows=1,dtype=str,delimiter='\t')))
        try:
            self.init_table()
        except:
            print("Could not connect to server.")

    # checks if stock ticker is within list of known stocks
    def is_valid_stock(self,stock):
        if stock in self.__tickers:
            self.stock = stock
            return True
        return False
    
    # opens connection to db
    def connect_db(self):
        load_dotenv(find_dotenv())
        password = os.getenv('POSTGRES_PASSWORD')
        host = os.getenv('POSTGRES_HOST')
        try:
            conn = psycopg2.connect(dbname='forecastdb',user='postgres',password=password,host=host,port='5432')
            return conn
        except psycopg2.Error as error:
            print("Unable to connect to the database")
            print(error)

    # initializes table with ticker and company names
    def init_table(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Stocks (
                ticker VARCHAR(10) PRIMARY KEY,
                name VARCHAR(1000)
            );
        """)

        for record in self.__tickers:
            cursor.execute("""INSERT INTO Stocks (ticker, name) 
                              VALUES (%s, %s) 
                              ON CONFLICT (ticker) DO NOTHING;""", (record[0],record[1]))
        
        conn.commit()
        cursor.close()
        conn.close()