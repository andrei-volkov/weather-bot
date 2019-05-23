import pymongo

CLUSTER_URL = 'mongodb+srv://anrix:uh28IkToDvmTd2aG@cluster0-xqrtl.mongodb.net/admin'
DB_NAME = 'all_data'
COLLECTION_NAME = 'users'

client = pymongo.MongoClient(CLUSTER_URL)
users = client[DB_NAME][COLLECTION_NAME]
users_cities = {}

USER_ID_KEY = 'user_id'
CITY_KEY = 'city'


def init():
    for u in users.find({}):
        print(u)
        users_cities[u[USER_ID_KEY]] = u[CITY_KEY]


def add(chat_id, city):
    users_cities[chat_id] = city
    users.insert({USER_ID_KEY: chat_id, CITY_KEY: city})
