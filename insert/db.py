import datetime
import os
import sqlite3
from sqlite3 import Error
from constants.system import Global

import pandas as pd

# -> SE442 DB # SE442 DB # SE442 DB # SE442 DB # SE442 DB ->

class Database:

    def __int__(self):
        columns = [
            'Entry',
        ]
        self.rows = [columns]

    @staticmethod
    def set():
        check = False
        global conn

        try:
            conn = sqlite3.connect(f'../databases/{Global.__INSERT_DB_NAME__}')
            print("Database connection is successful!")

            c = conn.cursor()

            # verileri tabloya ekle

            c.execute(
                "CREATE TABLE IF NOT EXISTS eksi_table (id INTEGER PRIMARY KEY AUTOINCREMENT, Entry TEXT)")
            print("Table created successfully!")
            conn.commit()
            conn.close()

            check = True

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")
            return check

    @staticmethod
    def get():
        check = False
        global c
        global rows
        global conn

        try:
            conn = sqlite3.connect(f'../databases/{Global.__INSERT_DB_NAME__}')
            print("Database connection is successful!")

            c = conn.cursor()

            c.execute(
                "SELECT Entry FROM eksi_table")
            rows = c.fetchall()
            print("Get data is successful!")
            conn.commit()
            conn.close()

            check = True

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

        finally:

            if conn:
                conn.close()
                print("The SQLite connection is closed")
            return rows, check
