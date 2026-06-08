import pytest
from fastapi.testclient import TestClient
from piccolo.utils.sync import run_sync

from steerer.main import app
from steerer.tables import UrlRoute


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def truncate_tables():
    run_sync(UrlRoute.delete(force=True).run())
    yield
