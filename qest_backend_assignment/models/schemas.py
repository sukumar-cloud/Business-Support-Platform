import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date, datetime

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    enrolled_services: Optional[List[str]] = []
    status: Optional[str] = "active"
    dob: Optional[date]
    created_at: Optional[date] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: str = Field(..., alias="_id")

class OrderBase(BaseModel):
    client_id: str
    service: str
    amount: float
    status: Optional[str] = "pending"
    created_at: Optional[datetime] = None

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: str = Field(..., alias="_id")

class PaymentBase(BaseModel):
    order_id: str
    amount_paid: float
    status: str
    date: Optional[datetime] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: str = Field(..., alias="_id")

class CourseBase(BaseModel):
    name: str
    instructor: str
    status: str
    start_date: date
    end_date: date

class CourseResponse(CourseBase):
    id: str = Field(..., alias="_id")

class ClassBase(BaseModel):
    course_id: str
    date: date
    time: str
    instructor: str
    status: str

class ClassResponse(ClassBase):
    id: str = Field(..., alias="_id")

class AttendanceBase(BaseModel):
    class_id: str
    client_id: str
    attended: bool

class AttendanceResponse(AttendanceBase):
    id: str = Field(..., alias="_id")

class QueryRequest(BaseModel):
    prompt: str

