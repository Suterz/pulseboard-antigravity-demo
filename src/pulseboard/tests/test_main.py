import pytest
from fastapi.testclient import TestClient

from pulseboard.main import app
from pulseboard.database import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure the database is initialized before tests"""
    init_db()
    yield


def test_read_main_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Pulseboard Dashboard" in response.text
    assert "mainChart" in response.text


def test_read_chart_data():
    response = client.get("/api/charts/data")
    assert response.status_code == 200
    data = response.json()
    assert "labels" in data
    assert "values" in data

    # Check default seeded data
    assert len(data["labels"]) == 4
    assert data["labels"] == ["Jan", "Feb", "Mar", "Apr"]
    assert data["values"] == [10, 25, 40, 35]
