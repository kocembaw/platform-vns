def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_experiments(client):
    response = client.get("/experiments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "exp-001"
    assert data[0]["session_count"] == 1


def test_get_experiment(client):
    response = client.get("/experiments/exp-001")
    assert response.status_code == 200
    body = response.json()
    assert body["protocol"] == "taVNS-A"
    assert len(body["sessions"]) == 1


def test_get_experiment_not_found(client):
    assert client.get("/experiments/does-not-exist").status_code == 404


def test_get_session(client):
    response = client.get("/sessions/sess-0001")
    assert response.status_code == 200
    assert response.json()["hrv_rmssd_ms"] == 42.1


def test_get_session_not_found(client):
    assert client.get("/sessions/does-not-exist").status_code == 404
