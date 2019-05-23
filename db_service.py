import pymongo

CLUSTER_URL = 'mongodb+srv://anrix:uh28IkToDvmTd2aG@cluster0-xqrtl.mongodb.net/admin'
DB_NAME = 'all_data'
COLLECTION_NAME = 'users'

client = pymongo.MongoClient(CLUSTER_URL)
users = client[DB_NAME][COLLECTION_NAME]


def get_all_users():
    return users.find({})
