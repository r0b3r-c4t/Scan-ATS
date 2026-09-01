from gridfs import GridFS
from pymongo import MongoClient

from app.config.settings import DATABASE_NAME, MONGO_URI


client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

grid_fs = GridFS(database)


def check_database_connection():
    client.admin.command("ping")
    return True