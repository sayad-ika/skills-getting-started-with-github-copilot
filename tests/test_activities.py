"""
Tests for the /activities endpoint.

Tests cover the GET /activities endpoint which returns all available
extracurricular activities with their details.
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Expected activity names based on src/app.py
EXPECTED_ACTIVITIES = [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Basketball Team",
    "Tennis Club",
    "Art Studio",
    "Drama Club",
    "Debate Team",
    "Science Club"
]


class TestGetActivities:
    """Test cases for GET /activities endpoint"""

    def test_get_activities_returns_200(self):
        """Test that /activities endpoint returns 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self):
        """Test that /activities endpoint returns a dictionary"""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_all_activities(self):
        """Test that all 9 expected activities are returned"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name in EXPECTED_ACTIVITIES:
            assert activity_name in activities, f"Activity '{activity_name}' not found in response"

    def test_get_activities_returns_correct_count(self):
        """Test that exactly 9 activities are returned"""
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 9

    def test_activity_has_required_fields(self):
        """Test that each activity has all required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, \
                    f"Activity '{activity_name}' missing required field: '{field}'"

    def test_activity_description_is_string(self):
        """Test that description field is a string"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"Activity '{activity_name}' description is not a string"
            assert len(activity_data["description"]) > 0, \
                f"Activity '{activity_name}' description is empty"

    def test_activity_schedule_is_string(self):
        """Test that schedule field is a string"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["schedule"], str), \
                f"Activity '{activity_name}' schedule is not a string"
            assert len(activity_data["schedule"]) > 0, \
                f"Activity '{activity_name}' schedule is empty"

    def test_activity_max_participants_is_positive_integer(self):
        """Test that max_participants is a positive integer"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity '{activity_name}' max_participants is not an integer"
            assert activity_data["max_participants"] > 0, \
                f"Activity '{activity_name}' max_participants is not positive"

    def test_activity_participants_is_list(self):
        """Test that participants field is a list"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"

    def test_activity_participants_are_strings(self):
        """Test that all participants are strings (emails)"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"Activity '{activity_name}' has non-string participant: {participant}"

    def test_current_participants_within_capacity(self):
        """Test that current_participants don't exceed max_participants"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            current = len(activity_data["participants"])
            max_capacity = activity_data["max_participants"]
            assert current <= max_capacity, \
                f"Activity '{activity_name}' has {current} participants but max is {max_capacity}"

    def test_specific_activity_chess_club_exists(self):
        """Test that Chess Club has expected data"""
        response = client.get("/activities")
        activities = response.json()
        
        assert "Chess Club" in activities
        chess = activities["Chess Club"]
        assert chess["max_participants"] == 12
        assert isinstance(chess["participants"], list)
        assert len(chess["participants"]) >= 0

    def test_specific_activity_programming_class_exists(self):
        """Test that Programming Class has expected data"""
        response = client.get("/activities")
        activities = response.json()
        
        assert "Programming Class" in activities
        programming = activities["Programming Class"]
        assert programming["max_participants"] == 20
        assert isinstance(programming["participants"], list)

    def test_specific_activity_science_club_exists(self):
        """Test that Science Club has expected data"""
        response = client.get("/activities")
        activities = response.json()
        
        assert "Science Club" in activities
        science = activities["Science Club"]
        assert science["max_participants"] == 22
        assert isinstance(science["participants"], list)
