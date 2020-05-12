import pymongo

db_client1 = pymongo.MongoClient("mongodb://10.6.0.2:27017/")
collection1 = db_client1["test_base"]["test_collection"]

db_client2 = pymongo.MongoClient("mongodb://10.6.0.3:27017/")
db_client2.drop_database("test_base")
collection2 = db_client2["test_base"]["test_collection"]

while collection2.find().count() < collection1.find().count():
    rand = list(collection1.aggregate([{"$sample": {'size': 1}}]))[0]
    found = collection2.find(rand)
    if found.count() == 0:
        collection2.insert_one(rand)
