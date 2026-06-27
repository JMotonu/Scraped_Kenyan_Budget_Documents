from pymongo import MongoClient
from config import *

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

collection = db[COLLECTION_NAME]


def save_document(document):

    existing = collection.find_one(
        {"url": document["url"]}
    )

    if not existing:
        collection.insert_one(document)


def get_documents():

    return list(collection.find())


def get_document_by_title(title):

    return collection.find_one(
        {"title": title}
    )


def delete_document(doc_id):

    from bson import ObjectId

    collection.delete_one(
        {"_id": ObjectId(doc_id)}
    )


def mark_viewed(doc_id):

    from bson import ObjectId

    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {"viewed": True}}
    )
    def get_documents_count():
        return collection.count_documents({})