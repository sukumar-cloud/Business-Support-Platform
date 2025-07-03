import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.mongodb_tool import (
    get_total_revenue, get_outstanding_payments, get_active_clients, get_inactive_clients,
    get_new_clients_this_month, get_top_services, get_enrollment_trends
)

def handle_dashboard_prompt(prompt: str):
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
            names = [s.get("service_name") or str(s) for s in top_services]
            return f"Top services: {', '.join(names)}"
        return "No top services found."

    if "enrollment trend" in prompt:
        trends = get_enrollment_trends()
        if trends:
            return f"Enrollment trends:\n{json.dumps(trends, indent=2)}"
        return "No enrollment trend data available."

    return "Sorry, I couldn't understand your dashboard request."
