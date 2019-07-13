import pymongo
from bson.objectid import ObjectId

uri = 'mongodb://duyvukhanh:123456a@ds059125.mlab.com:59125/vukhanhduy'

client = pymongo.MongoClient(uri)
db = client.vukhanhduy
question_list = db.questions
product_list = db.products


def insert_question(product:str,question: str, answer: str):
    question_list.insert_one({"product":product,"question":question,"answer":answer})

def get_question_by_product(product: str):
    return list(question_list.find({"product":product}))

def get_question_by_product_and_question(product: str,question:str):
    return question_list.find_one({"product":product,"question":question})

def get_all_questions():
    return list(question_list.find())

def delete_question(question_id):
    question_list.delete_one({"_id":ObjectId(question_id)})



def insert_product(product:str):
    product_list.insert_one({"product":product})

def get_all_products():
    return list(product_list.find())

# a = "product 2"
# b = "This is question 2"
# c = "This is answer for qs 2"

# insert_question("product 3","This is question 2","dit me ha")

# insert_product('product 3')
# print(get_question_by_product_and_question('product 1','This is question 1'))