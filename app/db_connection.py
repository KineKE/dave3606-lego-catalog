"""
Module text goes here.
"""

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = None
        self.port = None
        self.name = None
        self.user = None
        self.password = None
        self.connection = None
        self.cursor = None

    def __repr__(self):
        return f"Database ('{self.host, self.post, self.name}')"



    def get_db_config(self):
        pass

    def get_cursor(self):
        pass

    def get_connection(self):
        pass


    # def get_db_config(self):
    #     #TODO: Check for missing values
    #     return psycopg.connect(
    #         host=os.getenv("DB_HOST"),
    #         port=int(os.getenv("DB_PORT")),
    #         dbname=os.getenv("POSTGRES_DB"),
    #         user=os.getenv("POSTGRES_USER"),
    #         password=os.getenv("POSTGRES_PASSWORD")
    #     )