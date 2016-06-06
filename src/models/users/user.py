from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserError
import src.models.users.constants as UserConstant
import uuid

class User:

    def __init__(self, username, password, email, _id=None):
        self.username = username
        self.password = password
        self.email = email
        self._id = uuid.uuid4().hex if _id is None else _id


    def json(self):
        return {
            'username':self.username,
            'password':self.password,
            'email':self.email,
            '_id':self._id
        }


    def save_to_mongo(self):
        Database.update(UserConstant.COLLECTION, {'_id':self._id}, self.json())

    @staticmethod
    def is_valid_login(username, password):
        user_data = Database.find_one(UserConstant.COLLECTION, {'username':username})
        if user_data is None:
            raise UserError.UserNotExist("User is not existing in the database")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserError.PasswordIncorrect("Password is not correct")
        return True

    @staticmethod
    def register_user(username, password, email):
        user_data = Database.find_one(UserConstant.COLLECTION, {'username':username})
        if user_data is not None:
            raise UserError.UserIsExist("The user is existing in the database")
        if not Utils.email_is_valid(email):
            raise UserError.EmailNotValid("Email is not valid")
        password = Utils.hash_password(password)
        user = User(username, password, email)
        user.save_to_mongo()
        return True

    @classmethod
    def find_by_username(cls,username):
        return cls(** Database.find_one(UserConstant.COLLECTION, {'username':username}))

    @staticmethod
    def add_friends():
        pass

    @staticmethod
    def search_friend():
        pass

    @staticmethod
    def view_friends():
        pass

    @staticmethod
    def edit_user():
        pass



