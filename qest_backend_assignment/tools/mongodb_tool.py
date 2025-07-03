import sys
import os
from functools import lru_cache

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import (
    clients_column,
    orders_column,
    payments_column,
    courses_column,
    classes_column,
    attendance_column
)
from datetime import datetime, date
from collections import Counter

_client_cache = {}

def get_client_by_identifier(identifier: str):
    if identifier in _client_cache:
        return _client_cache[identifier]
    result = clients_column.find_one({
        "$or": [
            {"name": identifier},
            {"email": identifier},
            {"phone": identifier}
        ]
    })
    if result:
        _client_cache[identifier] = result
    return result

def get_active_clients():
    return list(clients_column.find({"status": "active"}))

def get_inactive_clients():
    return list(clients_column.find({"status": "inactive"}))

def get_new_clients_this_month():
    today = datetime.today()
    return list(clients_column.find({
        "created_at": {
            "$gte": date(today.year, today.month, 1).isoformat()
        }
    }))

def get_clients_with_birthdays_today():
    today = date.today()
    month = today.month
    day = today.day
    return list(clients_column.find({
        "$expr": {
            "$and": [
                {"$eq": [{"$month": {"$dateFromString": {"dateString": "$dob"}}}, month]},
                {"$eq": [{"$dayOfMonth": {"$dateFromString": {"dateString": "$dob"}}}, day]}
            ]
        }
    }))



def get_order_by_id(order_id: str):
    return orders_column.find_one({"_id": order_id})

def get_client_orders(client_id: str):
    return list(orders_column.find({"client_id": client_id}))

def get_orders_by_status(status: str):
    return list(orders_column.find({"status": status}))

def get_top_services(limit: int = 3):
    orders = orders_column.find()
    services = [o["service"] for o in orders]
    return Counter(services).most_common(limit)

def get_enrollment_trends():
    pipeline = [
        {"$group": {"_id": "$service", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    return list(orders_column.aggregate(pipeline))



def get_payment_by_order(order_id: str):
    return payments_column.find_one({"order_id": order_id})

@lru_cache(maxsize=16)
def get_total_revenue():
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount_paid"}}}]
    result = list(payments_column.aggregate(pipeline))
    return result[0]["total"] if result else 0

def get_outstanding_payments():
    return list(orders_column.find({"status": "pending"}))


def get_upcoming_classes():
    return list(classes_column.find({"status": "scheduled"}))

def get_classes_by_instructor(instructor: str):
    return list(classes_column.find({"instructor": instructor}))

def get_course_by_name(course_name: str):
    return courses_column.find_one({"name": course_name})

def get_active_courses():
    return list(courses_column.find({"status": "active"}))

def get_course_completion_rate(course_name: str):
    total_orders = orders_column.count_documents({"service": course_name})
    paid_orders = orders_column.count_documents({"service": course_name, "status": "paid"})
    return (paid_orders / total_orders * 100) if total_orders > 0 else 0


def get_attendance_percentage_by_class(class_id: str):
    total = attendance_column.count_documents({"class_id": class_id})
    attended = attendance_column.count_documents({"class_id": class_id, "attended": True})
    return (attended / total * 100) if total > 0 else 0

def get_class_dropoff_rate(class_id: str):
    total = attendance_column.count_documents({"class_id": class_id})
    missed = attendance_column.count_documents({"class_id": class_id, "attended": False})
    return (missed / total * 100) if total > 0 else 0
