# Multi-Agent Business Support Platform

A full-stack platform demonstrating AI-powered business support and analytics using CrewAI-style agents, MongoDB, FastAPI, and Streamlit.

---

## Overview
This project implements two intelligent backend agents:
- **Support Agent**: Handles natural language queries about services, orders, payments, and clients. Can create clients/orders and log enquiries.
- **Dashboard Agent**: Provides business analytics and metrics, such as revenue, client insights, service analytics, and attendance reports.

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
- **API**: `api/main.py` (routes queries to agents)
- **DB/Tools**: `tools/mongodb_tool.py`, `tools/external_api.py`, `config/db_config.py`
- **Frontend**: `frontend/streamlit_app.py`
- **Data/Models**: `data/*.json`, `models/schemas.py`

---

## File Structure
- `api/` — FastAPI app & endpoints
- `agents/` — Agent logic (support, dashboard)
- `tools/` — MongoDB and external API tools
- `models/` — Data schemas (Pydantic)
- `config/` — DB configuration
- `frontend/` — Streamlit UI
- `data/` — Mock data (JSON)
- `scripts/` — Data loading scripts

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

## Usage
- **Support Agent:**
  - Ask questions like:
    - `What classes are available this week?`
    - `Create a new client named Priya Sharma and place an order for Yoga Beginner.`
    - `Has order #12345 been paid?`
- **Dashboard Agent:**
  - Ask questions like:
    - `How much revenue did we generate this month?`
    - `Which course has the highest enrollment?`
    - `Show attendance percentage for Pilates.`

---
