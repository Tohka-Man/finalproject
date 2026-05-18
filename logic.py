import sqlite3
from datetime import datetime
from config import database 
import os
from typing import List, Tuple, Optional, Any

specialists = [ (_,) for _ in (['Программист', 'Отдел продаж'])]

class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            """conn.execute('''
            CREATE TABLE IF NOT EXISTS st_questions (
                id INTEGER PRIMARY KEY,
                question TEXT
                answer TEXT
            )
        ''')"""

            conn.execute('''
            CREATE TABLE IF NOT EXISTS specialists (
                id INTEGER PRIMARY KEY,
                specialist TEXT,
                opisanie TEXT
            )
        ''')

            conn.execute('''
            CREATE TABLE IF NOT EXISTS spec_questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                specialist TEXT,
                FOREIGN KEY(specialist) REFERENCES specialists(id)
            )
        ''')

            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO specialists (specialist) values(?)'
        data = specialists
        self.__executemany(sql, data)

    def insert_quest(self, data):
        sql = 'INSERT OR IGNORE INTO spec_questions (question, specialist) values(?, ?)'
        self.__executemany(sql, data)


    










