import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")
        self.conn = None

    def connection(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            return self.conn
        except pymysql.MySQLError as e:
            return None

    def close(self):
        if self.conn:
            self.conn.close()
