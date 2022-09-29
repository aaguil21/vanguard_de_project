#Includes database class and methods
#Used to establish connection to database and creation and querying of tables

import sqlite3
import pandas as pd
from pprint import pprint


class spotify_db:
    #Class used to make a daatabase object to facilitate connections and passing queries

    def __init__(self):
        #Conn extablishes connection to database file
        #Database cursor used to execute commands to database
        self.conn = self.load_db()
        self.cursor = self.conn.cursor()

    def load_db(self):
        #Create database if it doesn't exist, otherwise connect to it
        conn = sqlite3.connect("./spotify.db")
        return conn

    def add_table(self,table_name, df, data_type):
        #Create table in database from dataframe with given datatypes
        dtype = dict(zip(list(df.columns), data_type))
        df.to_sql(name=table_name, dtype=dtype, con=self.conn, if_exists='replace', index=False)
        self.conn.commit()
        return

    def query_view(self, query: str, view_name: str):
        #Creates a VIEW table within the database and then queries it to print columns
        #View_name must be the same as the one in query to create view
        self.cursor.execute(query)
        self.conn.commit()
        df = pd.read_sql_query(sql=f"SELECT * FROM {view_name}", con=self.conn)
        pprint(df.head(50))
        return df

    def query_to_df(self, query: str):
        #Saves the results of a query to a dataframe
        df = pd.read_sql_query(sql=query, con=self.conn)
        return df