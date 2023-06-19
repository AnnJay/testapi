from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

connection_string = os.environ.get("CONNECTION_STRING")

client = MongoClient(connection_string)
db = client.instruments_shop

categories_collection = db.categories
comments_collection = db.comments
instruments_collection = db.instruments


def fetch_all_categories():
    return list(categories_collection.find({}, {"_id": 0}))


def fetch_category_name(category_type):
    name = categories_collection.find_one(
        {"type": category_type}, {"_id": 0})["name"]

    if not name:
        return None

    return name


def fetch_instruments_by_category(category_type):
    responce_fields = {
        "_id": 0,
        "id": 1,
        "name": 1,
        "price": 1,
        "img_url": 1,
        "rating": 1
    }

    category_id = categories_collection.find_one({"type": category_type})["id"]

    return list(instruments_collection.find({"category_id": category_id}, responce_fields))


def fetch_instrument_by_id(id):
    return instruments_collection.find_one({"id": id}, {"_id": 0})


def fetch_comments_by_instrument_id(id):
    return list(comments_collection.find({"instrument_id": id}, {"_id": 0}))


def fetch_comments():
    return list(comments_collection.find({}, {"_id": 0}))


def insert_comment(comment):
    return comments_collection.insert_one(comment).inserted_id
