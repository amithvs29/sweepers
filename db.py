import cx_Oracle
import pandas
import logging


class Database(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def execute(self, query):
        logging.info('Executing query in ' + self.dbname)
        return pandas.read_sql(query, self.con)

    def use_db(self, dbname):
        self.dbname = dbname
        self.connect()

    def connect(self):
        try:
            self.con = cx_Oracle.connect(self.username, self.password, self.dbname)
            self.cur = self.con.cursor()
            logging.info('Connected to ' + self.dbname + ' database')
        except Exception as e:
            if 'ORA-01017' in str(e):
                logging.error('Unable to connect to ' + self.dbname + ' database. Invalid username/password')
                raise Exception("Invalid username/password")
            else:
                logging.error('Unable to connect to ' + self.dbname + ' database. Architecture mismatch(32bit vs 64bit)')
                raise Exception("Architecture mismatch(32bit vs 64bit)")
