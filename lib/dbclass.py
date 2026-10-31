from pymongo import MongoClient
from dotenv import load_dotenv
import os   
load_dotenv()
class Mdbconn:

    __MongoClient = None 

    @staticmethod
    def getMongoClient():
        if Mdbconn.__MongoClient is None:
            try:
                Mdbconn.__MongoClient = MongoClient(os.getenv('MONGO_URI')).get_database(os.getenv('MONGO_DB'))
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
        return Mdbconn.__MongoClient
