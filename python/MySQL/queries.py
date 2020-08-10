
import pymysql
from datetime import date, datetime, timedelta

#133
#need to sort out DB specific credentials

class Queries:
    """"
    General purpose database queries
    """
    def __init__(self):
        self.connection = pymysql.connect(host="", user="", passwd="", db="")

    def getConnection(self):
        return pymysql.connect(host="", user="", passwd="", db="")

    def query(self, code):
        """
        Queries database
        :param code:  to be sent to db
        :return:
        """
        cursor = self.connection.cursor()
        cursor.execute(f"{self.code}")
        return cursor.fetchall()[0][0]



    def getNUmberOfRecords(self, table):
        """
        connects to the database and sends an SQL request to it.
        SQL requests the number of records from * table
        :return: number of records in the prices table as an integer.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT count(*) FROM {self.table}")
        return cursor.fetchall()






