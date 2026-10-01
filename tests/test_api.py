from fastapi.testclient import TestClient

from textkit.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_slugify() -> None:
    r = client.post("/slugify", json={"text": "Привет, мир"})
    assert r.status_code == 200
    assert r.json() == {"slug": "privet-mir"}


def test_stats() -> None:
    r = client.post("/stats", json={"text": "a b a"})
    assert r.json() == {"characters": 5, "words": 3, "lines": 1, "top_words": [["a", 2], ["b", 1]]}


def test_validation_error() -> None:
    assert client.post("/slugify", json={}).status_code == 422
