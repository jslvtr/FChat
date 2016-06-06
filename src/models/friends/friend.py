import uuid
from src.common.database import Database
import src.models.friends.constants as FriendConstant

class Friends:

    def __init__(self, username, friend, _id):
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

