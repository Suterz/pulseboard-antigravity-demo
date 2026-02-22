import pytest
from fastapi.testclient import TestClient

from pulseboard.main import app
import pulseboard.database as db_module

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database(tmp_path, monkeypatch):
    """Ensure the database is initialized before tests in a temporary directory"""
    # Create a temporary sqlite file per test execution without data leakage
    test_db = tmp_path / "test_pulseboard.db"

    # Override the DB_PATH directly in the database module
    monkeypatch.setattr(db_module, "DB_PATH", test_db)

    # Initialize schema and seed data into the temporary database
    db_module.init_db()
    yield


def test_post_then_get_point():
    """POST /api/points then GET /api/points returns the created point"""
    payload = {"label": "Aug", "value": 85}
    post_res = client.post("/api/points", json=payload)
    assert post_res.status_code == 201

    # the ID should be 5 since 1-4 are the default seed
    created_id = post_res.json()["id"]

    get_res = client.get("/api/points")
    assert get_res.status_code == 200
    points = get_res.json()

    # Find the newly created point in the response
    found_point = next((p for p in points if p["id"] == created_id), None)
    assert found_point is not None
    assert found_point["label"] == "Aug"
    assert found_point["value"] == 85


def test_charts_derived_from_multiple_points_order():
    """Insert multiple points then GET /api/charts returns derived values in the expected order"""
    # Clear the default seed for easier assertion logic
    conn = db_module.get_db_connection()
    conn.execute("DELETE FROM metric_points")
    conn.commit()
    conn.close()

    # Insert test data sequentially
    client.post("/api/points", json={"label": "Point A", "value": 10})
    client.post("/api/points", json={"label": "Point B", "value": 20})
    client.post("/api/points", json={"label": "Point C", "value": 30})

    response = client.get("/api/charts/data")
    assert response.status_code == 200
    data = response.json()

    # Order should be chronological (ASC by ID), so A -> B -> C
    assert data["labels"] == ["Point A", "Point B", "Point C"]
    assert data["values"] == [10, 20, 30]


def test_charts_empty_db():
    """GET /api/charts handles empty DB by returning empty arrays"""
    # Clear the database entirely
    conn = db_module.get_db_connection()
    conn.execute("DELETE FROM metric_points")
    conn.commit()
    conn.close()

    response = client.get("/api/charts/data")
    assert response.status_code == 200
    data = response.json()
    assert data["labels"] == []
    assert data["values"] == []
