import ProjectCrypto.python.mongoDB.Mongo_Interaction_Connect_Query as mongolib
import os
import time


try:
    db_link = open("C:\\Users\\james\\Desktop\\db_info.txt", "r").read()
except:
    print("if you want the  connection to mongodb to work change the db_link on line 11")


def upload_files():
    db = mongolib.DB_Connection(db_link)
    db.connect_Client()
    for subdir, queryType in (('css', mongolib.QueryCSS), ('img', mongolib.QueryImage)):
        queryInstance = queryType(db.client)
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), '../..', subdir)):
            queryInstance.insert(os.path.join(os.path.join(os.path.dirname(__file__), '../..', subdir, filename)))
            print(f'inserted {filename}')


def main():
    upload_files()

main()