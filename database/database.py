# #(©)CodeXBotz




# import pymongo, os
# from config import DB_URI, DB_NAME


# dbclient = pymongo.MongoClient(DB_URI)
# database = dbclient[DB_NAME]


# user_data = database['users']



# async def present_user(user_id : int):
#     found = user_data.find_one({'_id': user_id})
#     return bool(found)

# async def add_user(user_id: int):
#     user_data.insert_one({'_id': user_id})
#     return

# async def full_userbase():
#     user_docs = user_data.find()
#     user_ids = []
#     for doc in user_docs:
#         user_ids.append(doc['_id'])
        
#     return user_ids

# async def del_user(user_id: int):
#     user_data.delete_one({'_id': user_id})
#     return



# db = dbclient['FSUB_BOT']

# def get_fsub_channels():
#     collection = db['fsub_channels']
#     channels = collection.find()
#     return [channel['channel_id'] for channel in channels]

# def add_fsub_channel(channel_id):
#     collection = db['fsub_channels']
#     collection.update_one({'channel_id': channel_id}, {'$set': {'channel_id': channel_id}}, upsert=True)

#(©)CodeXBotz

import pymongo
from config import DB_URI, DB_NAME

# Initialize the database client
dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

# Collection for user data
user_data = database['users']

# Asynchronous function to check if a user is present in the database
async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

# Asynchronous function to add a user to the database
async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

# Asynchronous function to get the full list of user IDs from the database
async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

# Asynchronous function to delete a user from the database
async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# Collection for forced subscription (FSUB) data
fsub_data = database['fsub_channels']
settings_data = database['settings']

# Function to get the list of forced subscription channels
def get_fsub_channels():
    channels = fsub_data.find()
    return [channel['channel_id'] for channel in channels]

# Function to add a channel to the forced subscription list
def add_fsub_channel(channel_id):
    fsub_data.update_one({'channel_id': channel_id}, {'$set': {'channel_id': channel_id}}, upsert=True)

# Function to remove a channel from the forced subscription list
def remove_fsub_channel(channel_id):
    fsub_data.delete_one({'channel_id': channel_id})

# Function to check if forced subscription is enabled
def is_fsub_enabled():
    setting = settings_data.find_one({'name': 'fsub_enabled'})
    if setting:
        return setting['value']
    return False

# Function to enable forced subscription
def enable_fsub():
    settings_data.update_one({'name': 'fsub_enabled'}, {'$set': {'value': True}}, upsert=True)

# Function to disable forced subscription
def disable_fsub():
    settings_data.update_one({'name': 'fsub_enabled'}, {'$set': {'value': False}}, upsert=True)


# def remove_fsub_channel(channel_id):
#     collection = db['fsub_channels']
#     collection.delete_one({'channel_id': channel_id})

