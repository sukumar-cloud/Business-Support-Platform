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

    match = re.search(r"(?:show|view|get) (?:enrolled services|services|status) for client ([\w ]+)", prompt_lc)
    if match:
        client_name = match.group(1).strip().title()
        client = get_client_by_identifier(client_name)
        if client:
            services = ', '.join(client.get('enrolled_services', []))
            status = client.get('status', 'unknown')
            return f"Client '{client_name}' is enrolled in: {services}. Status: {status}."
        return f"Client '{client_name}' not found."

    match = re.search(r"pending dues (?:for client ([\w ]+)|for order (\w+))", prompt_lc)
    if match:
        client_name = match.group(1)
        order_id = match.group(2)
        if client_name:
            client = get_client_by_identifier(client_name.title())
            if client:
                orders = get_client_orders(client['_id'])
                pending = [o for o in orders if o.get('status') == 'pending']
                total_due = sum(o.get('amount', 0) for o in pending)
                return f"Client '{client_name.title()}' has {len(pending)} pending order(s), total due: ₹{total_due}."
            return f"Client '{client_name.title()}' not found."
        elif order_id:
            order = get_order_by_id(order_id)
            if order and order.get('status') == 'pending':
                return f"Order #{order_id} is pending. Amount due: ₹{order.get('amount', 0)}."
            elif order:
                return f"Order #{order_id} is not pending."
            return f"Order #{order_id} not found."

    match = re.search(r"classes? (?:by|with) instructor ([\w ]+)", prompt_lc)
    if match:
        instructor = match.group(1).strip().title()
        classes = get_classes_by_instructor(instructor)
        if classes:
            class_list = [f"{c['date']} - {c.get('instructor', 'Unknown')}" for c in classes]
            return f"Classes by {instructor}:\n- " + "\n- ".join(class_list)
        return f"No classes found for instructor {instructor}."

    match = re.search(r"classes? with status ([\w]+)", prompt_lc)
    if match:
        status = match.group(1).strip().lower()
        classes = [c for c in get_upcoming_classes() if c.get('status', '').lower() == status]
        if classes:
            class_list = [f"{c['date']} - {c.get('instructor', 'Unknown')}" for c in classes]
            return f"Classes with status '{status}':\n- " + "\n- ".join(class_list)
        return f"No classes found with status '{status}'."

    return "Sorry, I couldn't understand your support request."
