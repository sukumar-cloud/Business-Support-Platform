# Business Support Platform

A full-stack platform demonstrating AI-powered business support and analytics using agents, MongoDB, FastAPI, and Streamlit.

---

## Overview
This project implements two intelligent backend agents:
- **Support Agent**: Handles natural language queries about services, orders, payments and clients. Can create clients/orders and log enquiries.
- **Dashboard Agent**: Provides business analytics and metrics, such as revenue, client insights, service analytics and attendance reports.

Agents interact with MongoDB (mock or real), external APIs, and expose endpoints via FastAPI. The Streamlit frontend offers a user-friendly interface for real-time interaction and visualization.

---

## Features
- Natural language query handling for both support and analytics
- Modular agent architecture (easy to extend)
- Mock data and/or real MongoDB integration
- API endpoints for agent interaction (FastAPI)
- Modern, interactive frontend (Streamlit)
- Efficient state management (O(1) query/answer lookup)
- Interview-ready code and documentation

---

## Architecture
```
[User] ⇄ [Streamlit Frontend] ⇄ [FastAPI Backend] ⇄ [Agents] ⇄ [MongoDB/External APIs]
```
- **Agents**: `agents/support_agent.py`, `agents/dashboard_agent.py`
- **API**: `api/main.py`
- **DB/Tools**: `tools/mongodb_tool.py`, `tools/external_api.py`, `config/db_config.py`
- **Frontend**: `frontend/streamlit_app.py`
- **Data/Models**: `data/*.json`, `models/schemas.py`

---

## File Structure
- `api/` — FastAPI app & endpoints
- `agents/` — Agent logics
- `tools/` — MongoDB and external API tools
- `models/` — Data schemas
- `config/` — DB configuration
- `frontend/` — Streamlit for frontend
- `data/` — sample data
- `scripts/` — Data loading script

---

## Setup & Running
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure environment:**
   - Set MongoDB URI and any secrets in `.env`
3. **Run backend:**
   ```bash
   uvicorn api.main:app --reload
   ```
4. **Run frontend:**
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
5. **(Optional) Load sample data:**
   ```bash
   python scripts/load_data.py
   ```

---
## Example Queries

### Support Agent
- Show enrolled services for client Priya Sharma
- Get status for client Rahul Verma
- Has order #12345 been paid?
- Create an order for Yoga Beginner for client Priya Sharma
- Pending dues for client Priya Sharma
- Pending dues for order o1
- Payment info for order #12345

### Dashboard Agent
- What is the total revenue?
- How much revenue did we generate this month?
- How many outstanding payments are there?
- How many active clients do we have?
- How many inactive clients do we have?
- Show me birthday reminders
- How many new clients this month?
- What are the top services?
- Which course has the highest enrollment?

