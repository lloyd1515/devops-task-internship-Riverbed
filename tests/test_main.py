"""Minimal smoke tests. CI runs these."""

from unittest.mock import patch

from fastapi.testclient import TestClient


def _client():
    from app.main import app
    return TestClient(app)


def test_health_endpoint_responds():
    with patch("app.main.r") as mock_redis:
        mock_redis.ping.return_value = True
        response = _client().get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_visits_increments():
    with patch("app.main.r") as mock_redis:
        mock_redis.incr.return_value = 42
        response = _client().get("/visits")
    assert response.status_code == 200
    assert response.json() == {"visits": 42}


def test_visits_count():
    with patch("app.main.r") as mock_redis:
        mock_redis.get.return_value = b"100"
        response = _client().get("/visits/count")
    assert response.status_code == 200
    assert response.json() == {"visits": 100}


def test_visits_count_none():
    with patch("app.main.r") as mock_redis:
        mock_redis.get.return_value = None
        response = _client().get("/visits/count")
    assert response.status_code == 200
    assert response.json() == {"visits": 0}


def test_visits_reset():
    with patch("app.main.r") as mock_redis:
        response = _client().post("/visits/reset")
        mock_redis.set.assert_called_once_with("visits", 0)
    assert response.status_code == 200
    assert response.json() == {"visits": 0}


# Monkey Tests (testing edge cases, invalid methods, and paths)
def test_monkey_invalid_methods():
    # POST to /visits/count is not allowed
    response = _client().post("/visits/count")
    assert response.status_code == 405

    # GET to /visits/reset is not allowed
    response = _client().get("/visits/reset")
    assert response.status_code == 405


def test_monkey_nonexistent_routes():
    # Random endpoints should return 404
    response = _client().get("/visits/invalid_sub_path")
    assert response.status_code == 404


def test_monkey_random_query_params():
    # Querying endpoints with unexpected parameters should work normally
    with patch("app.main.r") as mock_redis:
        mock_redis.get.return_value = b"10"
        response = _client().get("/visits/count?random_param=test&fuzzy=123")
    assert response.status_code == 200
    assert response.json() == {"visits": 10}
