from pymongo import mongo_client, MongoClient
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

client = MongoClient(f"mongodb://{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}")
# trial is the database name i created for testing, later we can create another one for packet capture.
db = client[os.getenv("MONGO_DB")]


# Same with sample collection
collection = db[os.getenv("MONGO_COLLECTION")]