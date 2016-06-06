import datetime
import uuid
from src.common.database import Database
import src.models.seeds.constants as SeedConstant

class Seed:
    def __init__(self, title, content, image, user_id, private, time=datetime.datetime.utcnow(), _id=None):
        self.title = title
        self.content = content
        self.image = image
        self.private = private
        self.time = time
        self.user_id = user_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {

            'title':self.title,
            'content':self.content,
            'image':self.image,
            'private':self.private,
            'user_id':self.user_id,
            'time':self.time,
            '_id':self._id
        }

    def save_to_mongo(self):
        Database.update(SeedConstant.COLLECTION, {'_id':self._id}, self.json())

    @classmethod
    def find_by_user(cls,user_id):
        return [cls(**elem) for elem in Database.find(SeedConstant.COLLECTION, {'user_id':user_id})]

    @classmethod
    def find_by_id(cls, _id):
        return cls(**Database.find_one(SeedConstant.COLLECTION, {'_id':_id}))

    @staticmethod
    def delete(_id):
        Database.remove(SeedConstant.COLLECTION, {'_id':_id})