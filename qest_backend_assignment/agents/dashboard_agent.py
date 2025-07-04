import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.mongodb_tool import (
    get_total_revenue, get_outstanding_payments, get_active_clients, get_inactive_clients,
    get_new_clients_this_month, get_top_services, get_enrollment_trends,
    get_clients_with_birthdays_today, get_course_completion_rate,
    get_attendance_percentage_by_class, get_class_dropoff_rate
)

def handle_dashboard_prompt(prompt: str):
    if "birthday" in prompt:
        birthdays = get_clients_with_birthdays_today()
        if birthdays:
            names = [c['name'] for c in birthdays]
            return f"Today's birthdays: {', '.join(names)}"
        return "No client birthdays today."

    if "completion rate" in prompt and "course" in prompt:
        import re
        match = re.search(r"course ([\w ]+)", prompt)
        if match:
            course_name = match.group(1).strip().title()
            rate = get_course_completion_rate(course_name)
            return f"Course '{course_name}' completion rate: {rate:.2f}%"
        return "Please specify the course name."

    if ("attendance" in prompt and "class" in prompt) or ("attendance percentage" in prompt):
        import re
        match = re.search(r"class ([\w\d]+)", prompt)
        if match:
            class_id = match.group(1).strip()
            percent = get_attendance_percentage_by_class(class_id)
            return f"Attendance percentage for class {class_id}: {percent:.2f}%"
        return "Please specify the class ID."

    if "drop-off" in prompt or "drop off" in prompt:
        import re
        match = re.search(r"class ([\w\d]+)", prompt)
        if match:
            class_id = match.group(1).strip()
            rate = get_class_dropoff_rate(class_id)
            return f"Drop-off rate for class {class_id}: {rate:.2f}%"
        return "Please specify the class ID."
    prompt = prompt.lower()

    if "revenue" in prompt and ("this month" in prompt or "total" in prompt):
        revenue = get_total_revenue()
        return f"Total revenue: ₹{revenue if revenue else 0}"

    if "outstanding payment" in prompt or "pending payment" in prompt:
        payments = get_outstanding_payments()
        return f"Outstanding payments: {len(payments)} order(s) pending." if payments else "No outstanding payments."

    if "inactive client" in prompt:
        clients = get_inactive_clients()
        return f"Inactive clients: {len(clients)}" if clients else "No inactive clients found."

    if "active client" in prompt:
        clients = get_active_clients()
        return f"Active clients: {len(clients)}" if clients else "No active clients found."

    if "new client" in prompt and "this month" in prompt:
        clients = get_new_clients_this_month()
        return f"New clients this month: {len(clients)}" if clients else "No new clients this month."

    if "top service" in prompt:
        top_services = get_top_services()
        if top_services:
            names = [s[0] for s in top_services]
            return f"Top services: {', '.join(names)}"
        return "No top services found."

    if "enrollment trend" in prompt:
        trends = get_enrollment_trends()
        if trends:
            return f"Enrollment trends:\n{json.dumps(trends, indent=2)}"
        return "No enrollment trend data available."

    return "Sorry, I couldn't understand your dashboard request."
