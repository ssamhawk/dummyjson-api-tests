from typing import Any

from base.api.api_client import APIClient
from dummyjson.models.user import User, UsersResponse


class UserClient:
    """Client for DummyJSON Users API"""

    def __init__(self, api_client: APIClient):
        self.api = api_client

    def get_all_users(self, limit: int = 30, skip: int = 0) -> UsersResponse:
        """Get all users with pagination"""
        response = self.api.get(f"/users?limit={limit}&skip={skip}")
        return UsersResponse.model_validate(response.json())

    def get_user_by_id(self, user_id: int) -> User:
        """Get a single user by ID"""
        response = self.api.get(f"/users/{user_id}")
        return User.model_validate(response.json())

    def search_users(self, query: str, limit: int = 30, skip: int = 0) -> UsersResponse:
        """Search users by query"""
        response = self.api.get(f"/users/search?q={query}&limit={limit}&skip={skip}")
        return UsersResponse.model_validate(response.json())

    def filter_users(self, key: str, value: str, limit: int = 30, skip: int = 0) -> UsersResponse:
        """Filter users by key-value pair"""
        response = self.api.get(f"/users/filter?key={key}&value={value}&limit={limit}&skip={skip}")
        return UsersResponse.model_validate(response.json())

    def add_user(self, user_data: dict[str, Any]) -> User:
        """Add a new user"""
        response = self.api.post("/users/add", json=user_data)
        return User.model_validate(response.json())

    def update_user(self, user_id: int, user_data: dict[str, Any]) -> User:
        """Update a user"""
        response = self.api.put(f"/users/{user_id}", json=user_data)
        return User.model_validate(response.json())

    def delete_user(self, user_id: int) -> User:
        """Delete a user"""
        response = self.api.delete(f"/users/{user_id}")
        return User.model_validate(response.json())
