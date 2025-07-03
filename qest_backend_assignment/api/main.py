import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.schemas import QueryRequest, OrderCreate
from agents.support_agent import handle_support_prompt
from agents.dashboard_agent import handle_dashboard_prompt

from tools.external_api import create_fake_order, create_fake_enquiry

from config.db_config import orders_column

app = FastAPI(
    title="Qest AI Backend",
    description="FastAPI backend for Qest AI multi-agent system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": " Qest app  is running."}

@app.post("/ask-support")
def ask_support(query: QueryRequest):
    result = handle_support_prompt(query.prompt)
    return {"response": result}

@app.post("/ask-dashboard")
def ask_dashboard(query: QueryRequest):
    result = handle_dashboard_prompt(query.prompt)
    return {"response": result}

@app.post("/create-order")
def create_order(data: OrderCreate):
    fake_order = create_fake_order(data.dict())
    orders_column.insert_one(fake_order)
    return {
        "message": "Order created successfully",
        "order": fake_order
    }

@app.post("/create-enquiry")
def create_enquiry(query: QueryRequest):
    fake_enquiry = create_fake_enquiry({"question": query.prompt})
    return {
        "message": " Enquiry logged",
        "enquiry": fake_enquiry
    }