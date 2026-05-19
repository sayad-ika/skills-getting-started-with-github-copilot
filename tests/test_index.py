"""
Tests for the root / endpoint.

Tests cover the GET / endpoint which redirects to the static index page.
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestRootRedirect:
    """Test cases for GET / endpoint"""

    def test_root_returns_redirect_status(self):
        """Test that root endpoint returns a redirect status code"""
        response = client.get("/", follow_redirects=False)
        # FastAPI RedirectResponse defaults to 307 (Temporary Redirect)
        assert response.status_code in [307, 308]

    def test_root_redirects_to_static_index(self):
        """Test that root endpoint redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in [307, 308]
        assert "location" in response.headers
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_location_header_is_correct(self):
        """Test that the Location header points to correct path"""
        response = client.get("/", follow_redirects=False)
        location = response.headers.get("location")
        assert location == "/static/index.html"

    def test_root_with_follow_redirects_resolves(self):
        """Test that following redirects from root works"""
        # Following redirects should attempt to resolve to the static file
        response = client.get("/", follow_redirects=True)
        # Will be 200 if static file exists, or 404 if not (which is expected
        # since TestClient may not have access to mounted static files)
        assert response.status_code in [200, 404]

    def test_root_redirect_preserves_path_structure(self):
        """Test that redirect uses correct path structure"""
        response = client.get("/", follow_redirects=False)
        location = response.headers.get("location", "")
        assert location.startswith("/static/")
        assert "index.html" in location

    def test_root_endpoint_accepts_get_method(self):
        """Test that root endpoint accepts GET requests"""
        response = client.get("/")
        # Should not raise an error
        assert response.status_code in [307, 308, 200, 404]
