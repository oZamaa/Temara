from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    (tmp_path / "index.html").write_text("<html>SPA</html>", encoding="utf-8")
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "app-abc123.js").write_text("console.log(1)", encoding="utf-8")
    (tmp_path / "favicon.svg").write_text("<svg/>", encoding="utf-8")
    secret = tmp_path.parent / "secret.txt"
    secret.write_text("top secret", encoding="utf-8")
    return TestClient(create_app(Settings(static_dir=tmp_path)))


def test_root_serves_index(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "SPA" in response.text
    assert response.headers["cache-control"] == "no-cache"


def test_unknown_spa_route_falls_back_to_index(client: TestClient) -> None:
    response = client.get("/kanban/42")
    assert response.status_code == 200
    assert "SPA" in response.text


def test_hashed_asset_is_served_with_long_cache(client: TestClient) -> None:
    response = client.get("/assets/app-abc123.js")
    assert response.status_code == 200
    assert "immutable" in response.headers["cache-control"]


def test_missing_asset_is_404_not_spa(client: TestClient) -> None:
    assert client.get("/assets/missing.js").status_code == 404


def test_api_still_works_next_to_frontend(client: TestClient) -> None:
    assert client.get("/api/v1/health").json() == {"status": "ok"}


def test_unknown_api_route_is_404_with_error_envelope(client: TestClient) -> None:
    response = client.get("/api/v1/nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


@pytest.mark.parametrize("path", ["/../secret.txt", "/%2e%2e/secret.txt", "/..%2fsecret.txt"])
def test_path_traversal_does_not_leak_files(client: TestClient, path: str) -> None:
    response = client.get(path)
    assert "top secret" not in response.text


def test_no_frontend_when_static_dir_unset() -> None:
    client = TestClient(create_app(Settings(static_dir=None)))
    assert client.get("/").status_code == 404
    assert client.get("/api/v1/health").status_code == 200


def test_missing_build_fails_fast(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="Frontend build not found"):
        create_app(Settings(static_dir=tmp_path / "nope"))
