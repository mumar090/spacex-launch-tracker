from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date, datetime

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
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    rocket_name: Optional[str] = None
    success: Optional[bool] = None
    launchpad_name: Optional[str] = None

class LaunchFrequency(BaseModel):
    monthly: Dict[str, int]
    yearly: Dict[str, int]

class StatisticsResponse(BaseModel):
    success_rate_by_rocket: Dict[str, float]
    launch_count_by_launchpad: Dict[str, int]
    launch_frequency: LaunchFrequency
