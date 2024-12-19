# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from .services.log_collector import LogCollector
from .models.models import LogEntry

# Initialize FastAPI app and LogCollector
app = FastAPI()
log_collector = LogCollector()

@app.get("/health/")
async def health():
    return {"message": "Health OK!"}

# Define an endpoint to collect logs
@app.post("/log/")
async def create_log(log: LogEntry):
    try:
        log_collector.add_log(log)
        return {"message": "Log entry added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define an endpoint to view all logs
@app.get("/logs/")
async def get_logs():
    return log_collector.get_logs()

