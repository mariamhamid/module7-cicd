from fastapi.testclient import TestClient
import pytest
from main import app


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)
   