import pymongo
from bson.objectid import ObjectId

uri = 'mongodb://duyvukhanh:123456a@ds059125.mlab.com:59125/vukhanhduy'

client = pymongo.MongoClient(uri)
db = client.vukhanhduy
option_list = db.options


def insert_option(option: str, reply: str):
    option_list.insert_one({"option":option,"reply":reply})

def get_option(option: str):
    return option_list.find_one({"option":option})

def get_all_options():
    return list(option_list.find())

def delete_option(option_id):
    option_list.delete_one({"_id":ObjectId(option_id)})


insert_option("hung bia","day la game hung bia")