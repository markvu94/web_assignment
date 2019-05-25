from pymongo import MongoClient

uri = "mongodb+srv://admin:admin@c4e29-cluster-06kp9.mongodb.net/test?retryWrites=true"

client = MongoClient(uri)

canhan_database = client.canhan_database
canhan_collection = canhan_database["canhan_collection"]
