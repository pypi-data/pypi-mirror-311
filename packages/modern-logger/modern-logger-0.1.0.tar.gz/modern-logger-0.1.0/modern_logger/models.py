"""Shared models for logging system."""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class LogEntry(BaseModel):
    level: str
    user_id: str
    action: str
    description: str
    component: str
    metadata: Optional[Dict] = None

class SearchQuery(BaseModel):
    query: Optional[str] = None
    level: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float
    metrics: Dict[str, Any]
