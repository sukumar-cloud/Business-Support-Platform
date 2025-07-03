import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.mongodb_tool import (
    get_client_by_identifier, get_order_by_id, get_client_orders, get_orders_by_status,
    get_payment_by_order, get_upcoming_classes, get_classes_by_instructor, get_course_by_name
)
from tools.external_api import create_fake_order, create_fake_enquiry

import re

def handle_support_prompt(prompt: str):
    prompt_lc = prompt.lower()

    if "class" in prompt_lc and ("available" in prompt_lc or "this week" in prompt_lc):
        classes = get_upcoming_classes()
        if classes:
            class_list = [f"{c['date']} - {c.get('instructor', 'Unknown')}" for c in classes]
            return f"Upcoming classes:\n- " + "\n- ".join(class_list)
        return "No upcoming classes found."

    if "order" in prompt_lc and "paid" in prompt_lc:
        order_id = ''.join(filter(str.isdigit, prompt_lc))
        order = get_order_by_id(order_id)
        if order:
            payment = get_payment_by_order(order_id)
            if payment:
                return f"Order #{order_id} payment status: {payment['status']}"
            return f"Payment info for Order #{order_id} not found."
        return f"Order #{order_id} not found."

    client_create_match = re.search(r"create (?:a )?new client named ([\w ]+)(?: with email ([\w@.]+))?(?: and phone (\d+))?", prompt_lc)
    if client_create_match:
        client_name = client_create_match.group(1).strip().title()
        client_email = client_create_match.group(2) if client_create_match.group(2) else None
        client_phone = client_create_match.group(3) if client_create_match.group(3) else None

        client = get_client_by_identifier(client_name)
        if client:
            msg = f"Client '{client_name}' already exists."
        else:
            client = {"name": client_name, "email": client_email, "phone": client_phone, "_id": client_name.replace(' ', '_').lower()}
            msg = f"Client '{client_name}' created successfully."

        order_match = re.search(r"order for ([\w ]+)", prompt_lc)
        if order_match:
            service = order_match.group(1).strip().title()
            order = create_fake_order({"client_id": client["_id"], "service": service, "amount": 2000})
            return msg + f" Order created for '{client_name}' with service '{service}'."
        return msg

    order_match = re.search(r"create (?:an )?order for ([\w ]+) for client ([\w ]+)", prompt_lc)
    if order_match:
        service = order_match.group(1).strip().title()
        client_name = order_match.group(2).strip().title()
        client = get_client_by_identifier(client_name)
        if client:
            order = create_fake_order({"client_id": client["_id"], "service": service, "amount": 2000})
            return f"Order created for '{client_name}' with service '{service}'."
        return f"Client '{client_name}' not found."

    if "enquiry" in prompt_lc or "enquire" in prompt_lc:
        enquiry = create_fake_enquiry({"question": prompt})
        print(" Enquiry created:", enquiry)
        return "Enquiry logged successfully."

    return "Sorry, I couldn't understand your support request."
