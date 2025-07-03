import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uuid import uuid4
from datetime import datetime

def create_fake_client(data: dict) -> dict:
    return {
        "_id": f"c_{uuid4().hex[:6]}",
        "created_at": datetime.now().date().isoformat(),
        **data
    }

def create_fake_order(data: dict) -> dict:
    return {
        "_id": f"o_{uuid4().hex[:6]}",
        "status": "pending",
        "created_at": datetime.now().date().isoformat(),
        **data
    }

def create_fake_enquiry(data: dict) -> dict:
    return {
        "enquiry_id": f"e_{uuid4().hex[:6]}",
        "submitted_at": datetime.now().isoformat(),
        **data
    }