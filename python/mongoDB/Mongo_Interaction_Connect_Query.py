import pymongo
import logging
import os
import bson

#enter address for cluster here:
cluster_address = ""

class DB_Connection:
    """
    connection object
    """

    def __init__(self):
        self.address = cluster_address
        self.port = 27017
        #27017 is default port for mongodb
        self.client = None


    def connect_Client(self):
        try:
            self.client = pymongo.MongoClient(self.address)
        except:
            logging.error("couldn't connect to address given")



class Query:
    """"
    query object.
    an instance of DB_connection is passed in upon an instance of Query's creation
    """
    database = 'webpage'

    def __init__(self, client_in):
        self.client = client_in

    def insert(self, doc):
        self.client[self.database][self.collection].insert_one(doc)


    def getOne(self, filter):
        return self.client[self.database][self.collection].find_one(filter)


class QueryImage(Query):
    collection = 'ímages'
    payloadKey = 'ímage'

    """"
    stores image as BSON object
    """

    def insert(self, pathToImage):
        with open(pathToImage, 'rb') as image:
            contents = image.read()
            filename = os.path.basename(pathToImage)
            self.client[self.database][self.collection].insert_one({'name': filename, self.payloadKey: bson.Binary(contents)})

    def getOne(self, filename):
        return self.client[self.database][self.collection].find_one({'name': filename})[self.payloadKey]


class QueryHTML(Query):
    collection = 'html'
    payLoadKey = 'html'

    def insert(self, pathToHtml):
        with open(pathToImage, 'r') as html:
            contents = image.read()
            filename = os.path.basename(pathToImage)
            self.client[self.database][self.collection].insert_one({'name': filename, self.payLoadKey: contents})

    def getOne(self, filename):
        return self.client[self.database][self.collection].find_one({'name': filename})[self.payLoadKey]


class QueryCSS(Query):
    collection = 'css'
    payloadKey = 'css'

class QueryJS(Query):
    collection = 'js'
    payloadKey = 'javaScript'

class QueryPHP(Query):
    collection = 'php'
    payloadKey = 'php'


def main():

    db = DB_Connection()
    db.address = cluster_address
    db.connect_Client()

    q = Query(db.client)
    q.change_db("test")
    q.insert('testcoll', {'akey': 'avalue', 'other': 'stuff'})


    i = q.getOne('testcoll', {'akey': 'avalue'})
    print(i)


main()