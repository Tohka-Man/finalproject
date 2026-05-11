import sqlite3
from datetime import datetime
from config import database 
import os
from typing import List, Tuple, Optional, Any

class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS st_questions (
                id INTEGER PRIMARY KEY,
                question TEXT
                answer TEXT
            )
        ''')

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
