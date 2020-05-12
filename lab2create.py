import pymongo
import sys

import random

my_list = [
    {"name": "Amy", "address": "Apple st 652"},
    {"name": "Hannah", "address": "Mountain 21"},
    {"name": "Michael", "address": "Valley 345"},
    {"name": "Sandy", "address": "Ocean blvd 2"},
    {"name": "Betty", "address": "Green Grass 1"},
    {"name": "Richard", "address": "Sky st 331"},
    {"name": "Susan", "address": "One way 98"},
    {"name": "Vicky", "address": "Yellow Garden 2"},
    {"name": "Ben", "address": "Park Lane 38"},
    {"name": "Kot", "address": "Central st 954"}
]

db_client = pymongo.MongoClient("mongodb://10.6.0.2:27017/")
db_client.drop_database("test_base")
collection = db_client["test_base"]["test_collection"]
try:
    collection.insert_many(my_list)
    for i in range(int(sys.argv[1])):
        for ii in range(10):
            collection.insert_one({"name": str(random.random()) + str(ii), "address": str(i) + str(ii)})
except Exception as bwe:
    print(bwe.details)
