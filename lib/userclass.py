try:
    from pymongo import MongoClient
    from mongogettersetter import MongoGetterSetter
except:
    print('Module\'s are not there ')
from .dbclass import Mdbconn
from bcrypt import hashpw, gensalt, checkpw
from pymongo.errors import DuplicateKeyError
from uuid import uuid4
from datetime import datetime , timezone
import random
from .errclass import DuplicateUserError , NotFoundUserError ,PasswordError
from mongogettersetter import MongoGetterSetter


db_conn = Mdbconn.getMongoClient()
db_user = db_conn.users

class UserCollection(metaclass=MongoGetterSetter):
    def __init__(self, username):
        self._collection = db_user
        self._filter_query = {"$or" : [{"id": username}, {"username": username}]}


class User:
    def __init__(self, id):
        self.collection = UserCollection(id)
        self.username = self.collection.username
        self.id = self.collection.id

    @staticmethod
    def find_mail(mail):
        return db_user.find_one({"email":mail})
            
    @staticmethod
    def login(user_info):
        try:
            result = User(user_info["username"])
        except Exception as e:
            return False

        stored_password = result.collection.password

        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        if checkpw(
            user_info["password"].encode("utf-8"),
            stored_password
        ):

            return True

        return False

        
        
        
        
    @staticmethod
    def signup(user_info):
        uuid = str(uuid4())

        if db_user.find_one({"username":user_info['username']}):
            False
        
        if db_user.find_one({"email":user_info['email']}):
            return False
        
        try:
            hashed_password = hashpw(user_info['password'].encode(), gensalt())
            db_user.insert_one({

                'id': uuid,
                'username': user_info['username'],
                'password': hashed_password,
                'email': user_info['email'],
                'created_at': datetime.now(timezone.utc),
                'active': False,
                'active_token': random.randint(100000, 999999)
            })

            return True
        except DuplicateKeyError as e:
            raise DuplicateUserError() 
        except Exception as e:
            raise ValueError("An error occurred during signup: " + str(e)) from e


