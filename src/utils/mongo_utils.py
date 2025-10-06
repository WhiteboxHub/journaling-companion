from pymongo import MongoClient
import os

# --- Mongo Connection ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "journaling_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collection references
journal_entries = db["journal_entries"]
users = db["users"]