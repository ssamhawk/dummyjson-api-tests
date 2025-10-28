import allure

from dummyjson.clients.auth_client import AuthClient


@allure.feature("Authentication API")
@allure.story("Login")
class TestLogin:
    @allure.title("Login with valid credentials")
    @allure.description("Verify that user can login with valid username and password")
    def test_login_success(self, auth_client: AuthClient, test_credentials: dict[str, str]):
        response = auth_client.login(username=test_credentials["username"], password=test_credentials["password"])

        assert response.accessToken, "Access token should not be empty"
        assert response.refreshToken, "Refresh token should not be empty"
        assert response.username == test_credentials["username"], "Username should match"
        assert response.id > 0, "User ID should be greater than 0"
        assert response.email, "Email should not be empty"
        assert response.firstName, "First name should not be empty"
        assert response.lastName, "Last name should not be empty"

    @allure.title("Login with custom expiration time")
    @allure.description("Verify that login works with custom token expiration time")
    def test_login_with_custom_expiration(self, auth_client: AuthClient, test_credentials: dict[str, str]):
        custom_expiration = 120  # 120 minutes

        response = auth_client.login(
            username=test_credentials["username"], password=test_credentials["password"], expires_in_mins=custom_expiration
        )

        assert response.accessToken, "Access token should not be empty"
        assert response.refreshToken, "Refresh token should not be empty"


@allure.feature("Authentication API")
@allure.story("Get Current User")
class TestGetCurrentUser:
    @allure.title("Get current authenticated user")
    @allure.description("Verify that authenticated user can retrieve their profile information")
    def test_get_current_user(self, auth_client: AuthClient, test_credentials: dict[str, str]):
        # First login to get access token
        login_response = auth_client.login(username=test_credentials["username"], password=test_credentials["password"])
        access_token = login_response.accessToken

        # Get current user with access token
        user = auth_client.get_current_user(access_token)

        assert user.id == login_response.id, "User ID should match login response"
        assert user.username == login_response.username, "Username should match login response"
        assert user.email == login_response.email, "Email should match login response"
        assert user.firstName, "First name should not be empty"
        assert user.lastName, "Last name should not be empty"


@allure.feature("Authentication API")
@allure.story("Refresh Token")
class TestRefreshToken:
    @allure.title("Refresh access token")
    @allure.description("Verify that access token can be refreshed using refresh token")
    def test_refresh_token(self, auth_client: AuthClient, test_credentials: dict[str, str]):
        # First login to get refresh token
        login_response = auth_client.login(username=test_credentials["username"], password=test_credentials["password"])
        refresh_token = login_response.refreshToken

        # Refresh the token
        refresh_response = auth_client.refresh_token(refresh_token)

        assert refresh_response.accessToken, "New access token should not be empty"
        assert refresh_response.refreshToken, "New refresh token should not be empty"
        assert refresh_response.accessToken != login_response.accessToken, "New access token should be different"

    @allure.title("Refresh token with custom expiration")
    @allure.description("Verify that token refresh works with custom expiration time")
    def test_refresh_token_with_custom_expiration(self, auth_client: AuthClient, test_credentials: dict[str, str]):
        # First login
        login_response = auth_client.login(username=test_credentials["username"], password=test_credentials["password"])
        refresh_token = login_response.refreshToken
        custom_expiration = 180  # 180 minutes

        # Refresh with custom expiration
        refresh_response = auth_client.refresh_token(refresh_token, expires_in_mins=custom_expiration)

        assert refresh_response.accessToken, "New access token should not be empty"
        assert refresh_response.refreshToken, "New refresh token should not be empty"
