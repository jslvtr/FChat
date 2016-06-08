from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserError
import src.models.users.constants as UserConstant
import uuid
from src.models.friends.friend import Friends

class User:

    def __init__(self, username, password, email, image, friends=[], _id=None):
        self.username = username
        self.password = password
        self.email = email
        self.image = image
        self.friends = friends
        self._id = uuid.uuid4().hex if _id is None else _id


    def json(self):
        return {
            'username':self.username,
            'password':self.password,
            'email':self.email,
            '_id':self._id,
            'friends':self.friends,
            'image':self.image
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
    def register_user(username, password, email, image):
        user_data = Database.find_one(UserConstant.COLLECTION, {'username':username})
        if user_data is not None:
            raise UserError.UserIsExist("The user is existing in the database")
        if not Utils.email_is_valid(email):
            raise UserError.EmailNotValid("Email is not valid")
        password = Utils.hash_password(password)
        user = User(username, password, email, image)
        user.save_to_mongo()
        return True

    @classmethod
    def find_by_username(cls,username):
        return cls(** Database.find_one(UserConstant.COLLECTION, {'username':username}))


    def add_friends(self, friend_name):
        friend = Friends(username=self.username, friend=friend_name)
        user = self.find_by_username(self.username)
        user.friends.append(friend_name)
        friend.save_to_mongo()
        user.save_to_mongo()

    @classmethod
    def search_friend(cls, search_term):
        return [ cls(**elem) for elem in Database.find(UserConstant.COLLECTION, {'username':{"$regex":search_term}}) ]

    @staticmethod
    def view_friends(username):
        return Friends.find_all_by_username(username)

    @staticmethod
    def edit_user():
        pass



