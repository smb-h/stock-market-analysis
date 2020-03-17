import pymongo 



client = pymongo.MongoClient('localhost', 27017)
# client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["stock_market"]
# if "statistics" in client.list_database_names():
#     print("db exists")

# collection
coll = db["symbols"]
# collist = db.list_collection_names()
# if "symbols" in collist:
#   print("The collection exists.")


data = { "name": "John", "address": "Highway 37" }
x = coll.insert_one(data)



print(client.list_database_names())
print(db.list_collection_names())

