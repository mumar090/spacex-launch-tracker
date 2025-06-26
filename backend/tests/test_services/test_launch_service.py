import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.coder import JsonCoder

from backend.services.launch_service import SpaceXService
from backend.models.models import Launch, Rocket, Launchpad


pytestmark = pytest.mark.asyncio

@pytest.fixture(autouse=True)
def init_cache():
    FastAPICache.init(InMemoryBackend(), coder=JsonCoder())

@pytest.fixture
def service():
    return SpaceXService()


@pytest.fixture
def sample_launches():
    return [
        Launch(id="1", name="Launch 1", date_utc=datetime(2022, 5, 15), success=True, rocket="rocket1", launchpad="pad1"),
        Launch(id="2", name="Launch 2", date_utc=datetime(2023, 6, 20), success=False, rocket="rocket2", launchpad="pad2"),
        Launch(id="3", name="Launch 3", date_utc=datetime(2023, 7, 10), success=True, rocket="rocket1", launchpad="pad1"),
    ]


@pytest.fixture
def sample_rockets():
    return [
        Rocket(id="rocket1", name="Falcon 9", success_rate_pct=90),
        Rocket(id="rocket2", name="Falcon Heavy", success_rate_pct=80),
    ]


@pytest.fixture
def sample_launchpads():
    return [
        Launchpad(id="pad1", name="LC-39A", launch_attempts=10),
        Launchpad(id="pad2", name="SLC-40", launch_attempts=5),
    ]


@pytest.mark.asyncio
async def test_fetch_launches(service):
    with patch.object(service, "_fetch", new=AsyncMock(return_value=[{
        "id": "1", "name": "L1", "date_utc": "2022-01-01T00:00:00Z", "success": True, "rocket": "r1", "launchpad": "p1"
    }])):
        launches = await service.fetch_launches()
        assert len(launches) == 1
        assert launches[0].name == "L1"


@pytest.mark.asyncio
async def test_filter_launches_by_rocket(service, sample_launches, sample_rockets, sample_launchpads):
    service.fetch_launches = AsyncMock(return_value=sample_launches)
    service.fetch_rockets = AsyncMock(return_value=sample_rockets)
    service.fetch_launchpads = AsyncMock(return_value=sample_launchpads)

    results = await service.filter_launches(rocket_name="Falcon 9")
    assert len(results) == 2
    assert all(r.rocket == "rocket1" for r in results)


@pytest.mark.asyncio
async def test_get_success_rate_by_rocket(service, sample_rockets):
    service.fetch_rockets = AsyncMock(return_value=sample_rockets)
    result = await service.get_success_rate_by_rocket()
    assert result == {"Falcon 9": 90, "Falcon Heavy": 80}


@pytest.mark.asyncio
async def test_get_launch_count_by_launchpad(service, sample_launchpads):
    service.fetch_launchpads = AsyncMock(return_value=sample_launchpads)
    result = await service.get_launch_count_by_launchpad()
    assert result == {"LC-39A": 10, "SLC-40": 5}


@pytest.mark.asyncio
async def test_get_launch_frequency(service, sample_launches):
    service.fetch_launches = AsyncMock(return_value=sample_launches)
    result = await service.get_launch_frequency()
    assert result["monthly"] == {"2022-05": 1, "2023-06": 1, "2023-07": 1}
    assert result["yearly"] == {"2022": 1, "2023": 2}
