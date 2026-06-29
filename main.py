from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# CORS - required by grader
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_6oa3imyn4wkxrwpfsngig65b"
EMAIL = "gangulysiddhartha22@gmail.com"

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: List[Event]

@app.post("/analytics")
async def analytics(request: AnalyticsRequest, x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    events = request.events
    total_events = len(events)
    unique_users = len(set(e.user for e in events))
    
    # Revenue only from positive amounts
    revenue = sum(e.amount for e in events if e.amount > 0)
    
    # Top user by positive amount sum
    user_revenue: Dict[str, float] = {}
    for e in events:
        if e.amount > 0:
            user_revenue[e.user] = user_revenue.get(e.user, 0) + e.amount
    
    top_user = max(user_revenue, key=user_revenue.get) if user_revenue else ""
    
    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": round(float(revenue), 2),
        "top_user": top_user
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
