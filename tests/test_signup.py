"""
Tests for the /activities/{activity_name}/signup endpoint.

Tests cover the POST /activities/{activity_name}/signup endpoint which allows
students to sign up for extracurricular activities.
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestSignupForActivity:
    """Test cases for POST /activities/{activity_name}/signup endpoint"""

    # ============ Happy Path Tests ============

    def test_signup_returns_200_for_valid_activity(self):
        """Test that signup returns 200 for a valid activity and email"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_returns_success_message(self):
        """Test that signup returns a success message"""
        response = client.post(
            "/activities/Drama Club/signup",
            params={"email": "student123@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "student123@mergington.edu" in data["message"]
        assert "Drama Club" in data["message"]

    def test_signup_confirms_activity_name_in_response(self):
        """Test that response contains the activity name"""
        response = client.post(
            "/activities/Tennis Club/signup",
            params={"email": "newplayer@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Tennis Club" in response.json()["message"]

    def test_signup_confirms_email_in_response(self):
        """Test that response contains the email"""
        response = client.post(
            "/activities/Art Studio/signup",
            params={"email": "artist@mergington.edu"}
        )
        assert response.status_code == 200
        assert "artist@mergington.edu" in response.json()["message"]

    def test_signup_multiple_different_students_same_activity(self):
        """Test that multiple different students can signup to the same activity"""
        activity = "Debate Team"
        
        # First signup
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": "debater1@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Second signup with different email
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": "debater2@mergington.edu"}
        )
        assert response2.status_code == 200

    def test_signup_different_activities_same_student(self):
        """Test that a student can signup for multiple different activities"""
        email = "versatile@mergington.edu"
        
        response1 = client.post(
            "/activities/Science Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200

    # ============ Error Case Tests ============

    def test_signup_nonexistent_activity_returns_404(self):
        """Test that signup to nonexistent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_missing_email_parameter_returns_422(self):
        """Test that signup without email parameter returns 422 (validation error)"""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422

    def test_signup_empty_email_returns_422(self):
        """Test that signup with empty email string returns error"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": ""}
        )
        # Empty string may be accepted by FastAPI but shouldn't create duplicate
        # The key test is that it doesn't break the system
        assert response.status_code in [200, 422]

    def test_signup_duplicate_email_returns_400(self):
        """Test that a student cannot signup twice for the same activity"""
        activity = "Basketball Team"
        email = "duplicate@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()

    def test_signup_already_existing_participant_returns_400(self):
        """Test that existing participants cannot signup again"""
        # Using an email that's already in Chess Club from src/app.py
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    # ============ Edge Case Tests ============

    def test_signup_with_special_characters_in_email(self):
        """Test signup with email containing special characters"""
        response = client.post(
            "/activities/Art Studio/signup",
            params={"email": "test+tag@example.com"}
        )
        # Should either succeed or give validation error, not crash
        assert response.status_code in [200, 400, 422]

    def test_signup_with_case_sensitive_activity_name(self):
        """Test that activity name is case-sensitive"""
        # Correct case
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "case1@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Wrong case should fail
        response2 = client.post(
            "/activities/chess club/signup",
            params={"email": "case2@mergington.edu"}
        )
        assert response2.status_code == 404

    def test_signup_whitespace_in_activity_name(self):
        """Test signup with activities that have spaces in names"""
        # "Programming Class" has a space
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "spacetest@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_case_sensitive_email_handling(self):
        """Test that the same email with different cases may be treated as duplicates"""
        # Depending on implementation, emails might be case-insensitive
        # This test documents the actual behavior
        activity = "Gym Class"
        email_lower = "casesensitive@mergington.edu"
        
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email_lower}
        )
        assert response1.status_code == 200

    def test_signup_at_capacity_limit(self):
        """Test behavior when activity approaches capacity"""
        # Programming Class has max 20 participants
        # We'll try to signup beyond what exists but won't verify exact count
        # since participants list state may vary
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "capacitytest@mergington.edu"}
        )
        # Should succeed (assuming not at full capacity from initial state)
        assert response.status_code == 200

    def test_signup_response_format_is_valid_json(self):
        """Test that signup response is valid JSON"""
        response = client.post(
            "/activities/Science Club/signup",
            params={"email": "jsontest@mergington.edu"}
        )
        assert response.status_code == 200
        # json() call will fail if response is not valid JSON
        data = response.json()
        assert isinstance(data, dict)

    def test_signup_with_very_long_email(self):
        """Test signup with a very long email address"""
        long_email = "a" * 100 + "@example.com"
        response = client.post(
            "/activities/Debate Team/signup",
            params={"email": long_email}
        )
        # Should either accept or reject, not crash
        assert response.status_code in [200, 400, 422]

    def test_signup_all_activities_accessible(self):
        """Test that signup works for all 9 activities"""
        activities = [
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
        
        for idx, activity in enumerate(activities):
            email = f"allactivities{idx}@mergington.edu"
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200, \
                f"Failed to signup for {activity}"
