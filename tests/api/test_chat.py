from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_lists_supported_figures() -> None:
    response = client.get("/api/v1/chat/figures")

    assert response.status_code == 200
    assert "Mahatma Gandhi" in response.json()["figures"]


def test_rejects_unknown_figure() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "figure": "Unknown Figure",
            "message": "Hello",
            "conversation_id": "e58d83ef-f1e5-4b47-b319-56e2eefcfc3e",
        },
    )

    assert response.status_code == 422
