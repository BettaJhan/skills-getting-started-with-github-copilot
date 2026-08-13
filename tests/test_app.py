from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_adds_new_participant():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.post("/activities/Chess Club/signup?email=alex@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up alex@mergington.edu for Chess Club"
    assert "alex@mergington.edu" in activities["Chess Club"]["participants"]

    activities["Chess Club"]["participants"] = original_participants


def test_signup_rejects_duplicate_email():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.post("/activities/Chess Club/signup?email=daniel@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    activities["Chess Club"]["participants"] = original_participants


def test_signup_rejects_full_activity():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    original_capacity = activities["Chess Club"]["max_participants"]
    activities["Chess Club"]["participants"] = [
        "user1@mergington.edu",
        "user2@mergington.edu",
        "user3@mergington.edu",
    ]
    activities["Chess Club"]["max_participants"] = 3

    # Act
    response = client.post("/activities/Chess Club/signup?email=user4@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"

    activities["Chess Club"]["participants"] = original_participants
    activities["Chess Club"]["max_participants"] = original_capacity


def test_unregister_removes_participant():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.delete("/activities/Chess Club/unregister?email=daniel@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]

    activities["Chess Club"]["participants"] = original_participants


def test_unregister_rejects_missing_participant():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
    ]

    # Act
    response = client.delete("/activities/Chess Club/unregister?email=daniel@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"

    activities["Chess Club"]["participants"] = original_participants
