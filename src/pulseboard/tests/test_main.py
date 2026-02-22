import pytest
from fastapi.testclient import TestClient

from pulseboard.main import app
from pulseboard.database import init_db, get_db_connection

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure the database is initialized before tests"""
    # Clear the database before each test to prevent state leakage
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS metric_points")
    conn.commit()
    conn.close()

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


def test_create_point():
    payload = {"label": "May", "value": 50}
    response = client.post("/api/points", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["label"] == "May"
    assert data["value"] == 50
    assert "id" in data

    # Verify via GET points
    get_response = client.get("/api/points")
    points = get_response.json()
    assert any(p["label"] == "May" for p in points)


def test_list_points():
    response = client.get("/api/points")
    assert response.status_code == 200
    points = response.json()
    assert len(points) == 4  # default seeded


def test_delete_point():
    # First create an item
    create_response = client.post("/api/points", json={"label": "July", "value": 70})
    item_id = create_response.json()["id"]

    # Now delete it
    delete_response = client.delete(f"/api/points/{item_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get("/api/points")
    points = get_response.json()
    assert not any(p["label"] == "July" for p in points)

    # Ensure deleting a non-existent item returns 404
    delete_missing_response = client.delete(f"/api/points/{item_id}")
    assert delete_missing_response.status_code == 404
