# https://api.mongodb.com/python/current/index.html


import pymongo
import pprint
from bson.objectid import ObjectId
from bson.son import SON
from bson.code import Code
import datetime
import pandas as pd


client = pymongo.MongoClient('localhost', 27017)
# client = pymongo.MongoClient("mongodb://localhost:27017/")

# DB
# db = client["test"]
db = client.test
dblist = client.list_database_names()
if "test" in client.list_database_names():
    print("db exists dropping db")
    client.drop_database('test')


# Collection
# coll_posts = db["posts"]
coll_posts = db.posts
collist = db.list_collection_names()
if "posts" in collist:
    print("The collection exists.")


# print collection as a df
col_data = list(coll_posts.find())
print(col_data) # this is as a json format
df_col_data = pd.DataFrame(col_data)
print(df_col_data)

# insert one
for i in range(10):
    data = {"name": f"John{str(i)}", "address": "Highway 37"}
    x = coll_posts.insert_one(data)
    x_id = x.inserted_id
    print(x)
    print(x_id)

# bulk insert
new_posts = [
    {
        "author": "Mike",
        "text": "Another post!",
        "tags": ["bulk", "insert"],
        "date": datetime.datetime(2009, 11, 12, 11, 14)
    },
    {
        "author": "Eliot",
        "title": "MongoDB is fun",
        "text": "and pretty easy too!",
        "date": datetime.datetime(2009, 11, 10, 10, 45)
    }]
result = coll_posts.insert_many(new_posts)
print(result.inserted_ids)
# Insert Multiple Documents, with Specified IDs
mylist = [
  { "_id": 1, "name": "John", "address": "Highway 37"},
  { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
  { "_id": 3, "name": "Amy", "address": "Apple st 652"},
  { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
  { "_id": 5, "name": "Michael", "address": "Valley 345"},
  { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
  { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
  { "_id": 8, "name": "Richard", "address": "Sky st 331"},
  { "_id": 9, "name": "Susan", "address": "One way 98"},
  { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
  { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
  { "_id": 12, "name": "William", "address": "Central st 954"},
  { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
  { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
]
# result = coll_posts.insert_many(mylist)
# print(result.inserted_ids)

# Query
pprint.pprint(db.posts.find_one())
pprint.pprint(coll_posts.find_one({"name": "John2"}))
pprint.pprint(coll_posts.find_one({"_id": x_id}))
# Note that an ObjectId is not the same as its string representation
pprint.pprint(coll_posts.find_one({"_id": ObjectId(str(x_id))}))

myquery = { "address": "Park Lane 38" }
mydoc = coll_posts.find(myquery)
for x in mydoc:
  print(x) 

# Querying for More Than One Document
for post in coll_posts.find():
    pprint.pprint(post)
# Search
for post in coll_posts.find({"_id": 0, "author": "Mike"}):
   pprint.pprint(post)


# Counting
print(coll_posts.count_documents({}))
print(coll_posts.count_documents({"author": "Mike"}))

# Range Queries
d = datetime.datetime(2009, 11, 12, 12)
for post in coll_posts.find({"date": {"$lt": d}}).sort("author"):
   pprint.pprint(post)
# exclude ids
for x in coll_posts.find({},{ "_id": 0, "name": 1, "address": 1 }):
    print(x)
# exclude addresses
for x in coll_posts.find({},{ "address": 0 }):
    print(x)
# You get an error if you specify both 0 and 1 values in the same object (except if one of the fields is the _id field)
# for x in coll_posts.find({},{ "name": 1, "address": 0 }):
#     print(x) 

# Indexing
result = db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)
print(sorted(list(db.profiles.index_information())))

# user_profiles = [
#         {'user_id': 211, 'name': 'Luke'},
#         {'user_id': 212, 'name': 'Ziltoid'}
#      ]
# result = db.profiles.insert_many(user_profiles)
# new_profile = {'user_id': 213, 'name': 'Drew'}
# duplicate_profile = {'user_id': 212, 'name': 'Tommy'}
# result = db.profiles.insert_one(new_profile)  # This is fine.
# Error
# result = db.profiles.insert_one(duplicate_profile)


# Advanced Query
# find the documents where the "address" field starts with the letter "S" or higher (alphabetically), use the greater than modifier: {"$gt": "S"}
# https://docs.mongodb.com/manual/reference/operator/query/
myquery = { "address": { "$gt": "S" } }
mydoc = coll_posts.find(myquery)
for x in mydoc:
    print(x) 

# Filter With Regular Expressions
myquery = { "address": { "$regex": "^S" } }
mydoc = coll_posts.find(myquery)
for x in mydoc:
    print(x) 


# sort
mydoc = coll_posts.find().sort("name", 1) #ascending
mydoc = coll_posts.find().sort("name", -1) #descending 
for x in mydoc:
    print(x) 



# Update Collection
# update first found
myquery = { "address": "Valley 345" }
newvalues = { "$set": { "address": "Canyon 123" } }
coll_posts.update_one(myquery, newvalues)
#print "customers" after the update:
for x in coll_posts.find():
    print(x) 


# Update Many
myquery = { "address": { "$regex": "^S" } }
newvalues = { "$set": { "name": "Minnie" } }
x = coll_posts.update_many(myquery, newvalues)
print(x.modified_count, "documents updated.") 


# Limit the Result
myresult = coll_posts.find().limit(5)
#print the result:
for x in myresult:
    print(x) 


# Aggregation Framework
# Aggregation operations process data records and return computed results. Aggregation operations group values from multiple documents together, and can perform a variety of operations on the grouped data to return a single result
pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
pprint.pprint(list(db.things.aggregate(pipeline)))
print(db.command('aggregate', 'things', pipeline=pipeline, explain=True))


# Map/Reduce
mapper = Code("""
               function () {
                 this.tags.forEach(function(z) {
                   emit(z, 1);
                 });
               }
               """)
reducer = Code("""
                function (key, values) {
                  var total = 0;
                  for (var i = 0; i < values.length; i++) {
                    total += values[i];
                  }
                  return total;
                }
                """)
# result = db.things.map_reduce(mapper, reducer, "myresults")
# for doc in result.find():
#     pprint.pprint(doc)
# pprint.pprint(db.things.map_reduce(mapper, reducer, "myresults", full_response=True))

# results = db.things.map_reduce(
#      mapper, reducer, "myresults", query={"x": {"$lt": 2}})
# for doc in results.find():
#    pprint.pprint(doc)

# You can use SON or collections.OrderedDict to specify a different database to store the result collection
# pprint.pprint(db.things.map_reduce(mapper, reducer, out=SON([("replace", "results"), ("db", "outdb")]), full_response=True))


# Delete document
# delete first found doc
myquery = { "address": "Mountain 21" }
coll_posts.delete_one(myquery)

# Delete Many Documents
myquery = { "address": {"$regex": "^S"} }
x = coll_posts.delete_many(myquery)
print(x.deleted_count, " documents deleted.") 

# Delete All Documents in a Collection
x = coll_posts.delete_many({})
print(x.deleted_count, " documents deleted.") 


# Delete Collection
# returns true false
coll_posts.drop() 

# drop db
# client.drop_database('test')






