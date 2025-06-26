from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date, datetime
from fastapi import Query

class Launch(BaseModel):
    id: str
    name: str
    date_utc: datetime
    success: Optional[bool]
    rocket: str
    launchpad: str

class LaunchListResponse(BaseModel):
    launches: List[Launch]

class Rocket(BaseModel):
    id: str
    name: str
    success_rate_pct: Optional[int] = None

class Launchpad(BaseModel):
    id: str
    name: str
    launch_attempts: Optional[int] = None

class LaunchFilterRequest(BaseModel):
    start_date: Optional[date] = Query(None, description="Filter launches after this date (YYYY-MM-DD)")
    end_date: Optional[date] = Query(None, description="Filter launches before this date (YYYY-MM-DD)")
    rocket_name: Optional[str] = Query(None, description="Name of the rocket")
    success: Optional[bool] = Query(None, description="Success status of the launch")
    launchpad_name: Optional[str] = Query(None, description="Name of the launchpad")

class LaunchFrequency(BaseModel):
    monthly: Dict[str, int]
    yearly: Dict[str, int]

class StatisticsResponse(BaseModel):
    success_rate_by_rocket: Dict[str, float]
    launch_count_by_launchpad: Dict[str, int]
    launch_frequency: LaunchFrequency
