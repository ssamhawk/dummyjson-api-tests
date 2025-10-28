from base.api.api_client import APIClient
from dummyjson.models.auth import LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from dummyjson.models.user import User


class AuthClient:
    """Client for DummyJSON Authentication API"""

    def __init__(self, api_client: APIClient):
        self.api = api_client

    def login(self, username: str, password: str, expires_in_mins: int = 60) -> LoginResponse:
        """Login and get access and refresh tokens"""
        login_data = LoginRequest(username=username, password=password, expiresInMins=expires_in_mins)
        response = self.api.post("/auth/login", json=login_data.model_dump())
        return LoginResponse.model_validate(response.json())

    def get_current_user(self, access_token: str) -> User:
        """Get current authenticated user"""
        response = self.api.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
        return User.model_validate(response.json())

    def refresh_token(self, refresh_token: str, expires_in_mins: int = 60) -> RefreshTokenResponse:
        """Refresh access token"""
        refresh_data = RefreshTokenRequest(refreshToken=refresh_token, expiresInMins=expires_in_mins)
        response = self.api.post("/auth/refresh", json=refresh_data.model_dump())
        return RefreshTokenResponse.model_validate(response.json())
