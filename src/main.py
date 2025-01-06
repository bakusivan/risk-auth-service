from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from .services.log_collector import LogCollector
from .services.risk_service import RiskService
from .models.models import LogEntry, RiskValues

# Initialize FastAPI app and services
app = FastAPI()
log_collector = LogCollector()
risk_service = RiskService()

@app.get("/health/")
async def health():
    return {"message": "Health OK!"}

# Define an endpoint to collect logs
@app.post("/log/")
async def create_log(log: LogEntry):
    try:
        log_collector.add_log(log)
        risk_service.process_log_chunk(log)  # Process the log to update risk data
        return {"message": "Log entry added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/logs/")
async def get_logs():
    return log_collector.get_logs()

@app.get("/risk/isuserknown")
async def is_user_known(username: str):
    try:
        risk_values = risk_service.get_user_risk(username)
        return {"is_user_known": risk_values.is_user_known}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/risk/isclientknown")
async def is_client_known(device_id: str):
    try:
        risk_values = risk_service.get_client_risk(device_id)
        return {"is_client_known": risk_values.is_client_known}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/risk/isipknown")
async def is_ip_known(ip: str):
    try:
        risk_values = risk_service.get_ip_risk(ip)
        return {"is_ip_known": risk_values.is_ip_known}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/risk/isipinternal")
async def is_ip_internal(ip: str):
    try:
        is_internal = risk_service.is_ip_internal(ip)
        return {"is_ip_internal": is_internal}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/risk/lastsuccessfullogindate")
async def last_successful_login_date(username: str):
    try:
        risk_values = risk_service.get_user_risk(username)
        return {"last_successful_login_date": risk_values.last_successful_login_date}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/risk/lastfailedlogindate")
async def last_failed_login_date(username: str):
    try:
        risk_values = risk_service.get_user_risk(username)
        return {"last_failed_login_date": risk_values.last_failed_login_date}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# TODO; not sure why total number of failed login attempts is not connected with the username
# but, it is clear from the "Proposed Solution" that we only need total int
@app.get("/risk/failedlogincountlastweek")
async def failed_login_count_last_week():
    try:
        total_failed_login_count = risk_service.get_failed_login_count_last_week()
        return {"failed_login_count_last_week": total_failed_login_count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
