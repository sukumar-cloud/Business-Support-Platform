import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME", "qest_db")


if not DB_URI:
    raise ValueError(" DB URl not found")

try:
    client = MongoClient(DB_URI)
    db = client[DB_NAME]
    clients_column = db["clients"]
    orders_column = db["orders"]
    payments_column = db["payments"]
    courses_column = db["courses"]
    classes_column = db["classes"]
    attendance_column = db["attendance"]


    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Failed to connect to database:{e}")