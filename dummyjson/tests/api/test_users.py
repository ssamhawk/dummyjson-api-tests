import allure
import pytest

from dummyjson.clients.user_client import UserClient


@allure.feature("Users API")
@allure.story("Get Users")
class TestGetUsers:
    @allure.title("Get all users with default pagination")
    @allure.description("Verify that API returns a list of users with correct pagination")
    def test_get_all_users(self, user_client: UserClient):
        response = user_client.get_all_users()

        assert response.total > 0, "Total users should be greater than 0"
        assert response.limit == 30, "Default limit should be 30"
        assert response.skip == 0, "Default skip should be 0"
        assert len(response.users) > 0, "Users list should not be empty"
        assert len(response.users) <= 30, "Users list should not exceed limit"

    @allure.title("Get users with custom pagination")
    @allure.description("Verify that API respects custom limit and skip parameters")
    @pytest.mark.parametrize("limit,skip", [(10, 0), (5, 10), (20, 40)])
    def test_get_users_with_pagination(self, user_client: UserClient, limit: int, skip: int):
        response = user_client.get_all_users(limit=limit, skip=skip)

        assert response.limit == limit, f"Limit should be {limit}"
        assert response.skip == skip, f"Skip should be {skip}"
        assert len(response.users) <= limit, "Users list should not exceed limit"

    @allure.title("Get single user by ID")
    @allure.description("Verify that API returns correct user by ID")
    def test_get_user_by_id(self, user_client: UserClient):
        user_id = 1
        user = user_client.get_user_by_id(user_id)

        assert user.id == user_id, f"User ID should be {user_id}"
        assert user.firstName, "User first name should not be empty"
        assert user.lastName, "User last name should not be empty"
        assert user.email, "User email should not be empty"
        assert user.username, "Username should not be empty"


@allure.feature("Users API")
@allure.story("Search Users")
class TestSearchUsers:
    @allure.title("Search users by query")
    @allure.description("Verify that API returns users matching search query")
    @pytest.mark.parametrize("query", ["John", "Emily", "Smith"])
    def test_search_users(self, user_client: UserClient, query: str):
        response = user_client.search_users(query=query)

        assert response.total >= 0, "Total should be non-negative"
        if response.total > 0:
            assert len(response.users) > 0, "Users list should not be empty when total > 0"

    @allure.title("Filter users by key-value pair")
    @allure.description("Verify that API returns filtered users by specific criteria")
    def test_filter_users(self, user_client: UserClient):
        response = user_client.filter_users(key="hair.color", value="Brown")

        assert response.total >= 0, "Total should be non-negative"
        if response.total > 0:
            assert len(response.users) > 0, "Users list should not be empty"
            # Verify all users have brown hair
            for user in response.users:
                assert user.hair.color == "Brown", "All filtered users should have brown hair"


@allure.feature("Users API")
@allure.story("Manage Users")
class TestManageUsers:
    @allure.title("Add new user")
    @allure.description("Verify that new user can be added")
    def test_add_user(self, user_client: UserClient):
        new_user = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
        }

        user = user_client.add_user(new_user)

        assert user.firstName == new_user["firstName"], "User first name should match"
        assert user.lastName == new_user["lastName"], "User last name should match"
        assert user.email == new_user["email"], "User email should match"
        assert user.username == new_user["username"], "Username should match"

    @allure.title("Update existing user")
    @allure.description("Verify that user can be updated")
    def test_update_user(self, user_client: UserClient):
        user_id = 1
        updated_data = {"firstName": "UpdatedName", "lastName": "UpdatedLastName"}

        user = user_client.update_user(user_id, updated_data)

        assert user.id == user_id, f"User ID should be {user_id}"
        assert user.firstName == updated_data["firstName"], "User first name should be updated"
        assert user.lastName == updated_data["lastName"], "User last name should be updated"

    @allure.title("Delete user")
    @allure.description("Verify that user can be deleted")
    def test_delete_user(self, user_client: UserClient):
        user_id = 1

        user = user_client.delete_user(user_id)

        assert user.id == user_id, f"Deleted user ID should be {user_id}"
