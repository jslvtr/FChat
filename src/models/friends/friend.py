import uuid
from src.common.database import Database
import src.models.friends.constants as FriendConstant

class Friends:

    def __init__(self, username, friend, _id=None):
        self.username = username
        self.friend = friend
        self._id = uuid.uuid4().hex if _id is None else _id


    def json(self):
        return {
            'username':self.username,
            'friend':self.friend,
            '_id':self._id
        }

    def save_to_mongo(self):
        Database.update(FriendConstant.COLLECTION, {'_id':self._id}, self.json())


    @classmethod
    def find_all_by_username(cls, username):
        return [cls(**elem) for elem in Database.find(FriendConstant.COLLECTION, {'username':username})]

    @staticmethod
    def delete(friend):
        Database.remove(FriendConstant.COLLECTION, {'friend':friend})

