import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import(
    clients_column,
    orders_column,
    payments_column,
    courses_column,
    classes_column,
    attendance_column
)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_data():

    clients_column.delete_many({})
    orders_column.delete_many({})
    payments_column.delete_many({})
    courses_column.delete_many({})
    classes_column.delete_many({})
    attendance_column.delete_many({})

    for doc in load_json("qest_backend_assignment/data/clients.json"):
        clients_column.replace_one({'_id': doc['_id']}, doc, upsert=True)
    for doc in load_json("qest_backend_assignment/data/orders.json"):
        orders_column.replace_one({'_id': doc['_id']}, doc, upsert=True)
    for doc in load_json("qest_backend_assignment/data/payments.json"):
        payments_column.replace_one({'_id': doc['_id']}, doc, upsert=True)
    for doc in load_json("qest_backend_assignment/data/courses.json"):
        courses_column.replace_one({'_id': doc['_id']}, doc, upsert=True)
    for doc in load_json("qest_backend_assignment/data/classes.json"):
        classes_column.replace_one({'_id': doc['_id']}, doc, upsert=True)
    for doc in load_json("qest_backend_assignment/data/attendance.json"):
        attendance_column.replace_one({'_id': doc['_id']}, doc, upsert=True)

    print(" data loaded successfully.")

if __name__ == "__main__":
    try:
        insert_data()
    except Exception as e:
        print(f" Error loading data: {e}")