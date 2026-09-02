from gridfs import GridFS
from pymongo import MongoClient

from app.config.settings import DATABASE_NAME, MONGO_URI


client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

grid_fs = GridFS(database)


candidates_collection = database["candidates"]
jobs_collection = database["jobs"]
analyses_collection = database["analyses"]

grid_fs = GridFS(database)