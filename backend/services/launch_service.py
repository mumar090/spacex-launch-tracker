import httpx
from typing import List, Dict, Optional
from fastapi import HTTPException
from fastapi_cache.decorator import cache
from collections import defaultdict


from backend.models.models import Launch, Rocket, Launchpad
from backend.config.config import settings

class SpaceXService:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=settings.BASE_URL)

    async def _fetch(self, endpoint: str):
        """
        Internal helper to fetch data from SpaceX API with error handling.
        Raises HTTPException on failure.
        """
        try:
            response = await self.client.get(endpoint)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error fetching {endpoint}: {exc.response.text}"
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Network error fetching {endpoint}: {str(exc)}"
            )

    @cache(expire=3600)
    async def fetch_launches(self) -> List[Launch]:
        data = await self._fetch("launches")
        return [Launch(**item) for item in data]

    @cache(expire=3600)
    async def fetch_rockets(self) -> List[Rocket]:
        data = await self._fetch("rockets")
        return [Rocket(**item) for item in data]

    @cache(expire=3600)
    async def fetch_launchpads(self) -> List[Launchpad]:
        data = await self._fetch("launchpads")
        return [Launchpad(**item) for item in data]
    
    async def filter_launches(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        rocket_name: Optional[str] = None,
        success: Optional[bool] = None,
        launchpad_name: Optional[str] = None,
    ) -> List[Launch]:
        raw_launches = await self.fetch_launches()
        launches = [Launch(**l) if isinstance(l, dict) else l for l in raw_launches]
        rockets = await self.fetch_rockets()
        launchpads = await self.fetch_launchpads()

        if start_date:
            launches = [l for l in launches if l.date_utc.date() >= start_date]

        if end_date:
            launches = [l for l in launches if l.date_utc.date() <= end_date]

        if rocket_name:
            rocket_ids = [r.id for r in rockets if r.name == rocket_name]
            launches = [l for l in launches if l.rocket in rocket_ids]

        if success is not None:
            launches = [l for l in launches if l.success == success]

        if launchpad_name:
            launchpad_ids = [p.id for p in launchpads if p.name == launchpad_name]
            launches = [l for l in launches if l.launchpad in launchpad_ids]

        return launches
    
    async def get_success_rate_by_rocket(self) -> Dict[str, int]:
        raw_rockets = await self.fetch_rockets()
        rockets = [r if isinstance(r, Rocket) else Rocket(**r) for r in raw_rockets]
        return {
            rocket.name: rocket.success_rate_pct or 0
            for rocket in rockets
        }

    
    async def get_launch_count_by_launchpad(self) -> Dict[str, int]:
        raw_launchpads = await self.fetch_launchpads()
        launchpads = [p if isinstance(p, Launchpad) else Launchpad(**p) for p in raw_launchpads]
        return {
            launchpad.name: launchpad.launch_attempts or 0
            for launchpad in launchpads
        }

    
    async def get_launch_frequency(self) -> Dict[str, Dict[str, int]]:
        raw_launches = await self.fetch_launches()
        launches = [l if isinstance(l, Launch) else Launch(**l) for l in raw_launches]

        monthly_counts = defaultdict(int)
        yearly_counts = defaultdict(int)

        for launch in launches:
            year = launch.date_utc.year
            month = launch.date_utc.month
            monthly_counts[f"{year}-{month:02d}"] += 1
            yearly_counts[str(year)] += 1

        return {
            "monthly": dict(monthly_counts),
            "yearly": dict(yearly_counts),
        }
