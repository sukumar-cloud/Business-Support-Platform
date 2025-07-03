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

    clients_column.insert_many(load_json("data/clients.json"))
    orders_column.insert_many(load_json("data/orders.json"))
    payments_column.insert_many(load_json("data/payments.json"))
    courses_column.insert_many(load_json("data/courses.json"))
    classes_column.insert_many(load_json("data/classes.json"))
    attendance_column.insert_many(load_json("data/attendance.json"))

    print(" data loaded successfully.")

if __name__ == "__main__":
    try:
        insert_data()
    except Exception as e:
        print(f" Error loading data: {e}")