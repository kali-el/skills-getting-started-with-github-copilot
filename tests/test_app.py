import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Baseline activities data for reset
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for interscholastic games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and compete in matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["sarah@mergington.edu", "james@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and develop acting skills",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["lisa@mergington.edu", "david@mergington.edu"]
    },
    "Art Class": {
        "description": "Explore painting, sculpture, and other visual arts",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu", "chris@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 20,
        "participants": ["ryan@mergington.edu", "natalie@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical thinking skills through competitive debate",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["tyler@mergington.edu", "jessica@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Fixture to reset activities state and provide a test client."""
    # Arrange: Reset activities to initial state
    activities.clear()
    activities.update(INITIAL_ACTIVITIES)
    
    yield TestClient(app)


def test_get_activities_returns_activities(client):
    """Test that GET /activities returns all activities with correct structure."""
    # Arrange
    expected_activity_count = len(INITIAL_ACTIVITIES)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == expected_activity_count
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    """Test that POST /activities/{activity}/signup adds a new participant."""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    """Test that signing up with a duplicate email returns 400."""
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity_removes_participant(client):
    """Test that DELETE /activities/{activity}/participants removes a participant."""
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    assert email_to_remove in activities[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity_name}"
    assert email_to_remove not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404(client):
    """Test that unregistering a nonexistent participant returns 404."""
    # Arrange
    activity_name = "Chess Club"
    nonexistent_email = "ghost@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": nonexistent_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
