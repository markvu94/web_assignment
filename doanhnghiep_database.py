from pymongo import MongoClient

uri = "mongodb+srv://admin:admin@c4e29-cluster-06kp9.mongodb.net/test?retryWrites=true"

client = MongoClient(uri)

user_database = client.user_database
user_collection = user_database["user_collection"]


