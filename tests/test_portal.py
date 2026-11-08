
import pytest
from app import app, submissions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    submissions.clear()

    with app.test_client() as test_client:
        yield test_client

    submissions.clear()


def test_valid_submission(client):
    response = client.post("/submit", json={
        "name": "Ujala Adil",
        "reg_number": "FA23-BAI-045",
        "title": "DevOps Lab Mid",
        "url": "https://github.com/ujalaadil1554/my-portfolio"
    })

    assert response.status_code == 200
    assert response.json["success"] is True

    list_response = client.get("/submissions")
    assert list_response.status_code == 200
    assert len(list_response.json) == 1
    assert list_response.json[0]["reg_number"] == "FA23-BAI-045"


def test_missing_registration_number(client):
    response = client.post("/submit", json={
        "name": "Ujala Adil",
        "reg_number": "",
        "title": "DevOps Lab Mid",
        "url": "https://github.com/ujalaadil1554/my-portfolio"
    })

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Registration number" in response.json["message"]
    assert len(client.get("/submissions").json) == 0


def test_invalid_url(client):
    response = client.post("/submit", json={
        "name": "Ujala Adil",
        "reg_number": "FA23-BAI-045",
        "title": "DevOps Lab Mid",
        "url": "invalid-url"
    })

    assert response.status_code == 400
    assert response.json["success"] is False
    assert len(client.get("/submissions").json) == 0
