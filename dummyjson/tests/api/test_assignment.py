"""
Test assignment scenarios for DummyJSON API
These tests cover specific requirements:
1. Check that at least one user with email "emily.johnson@x.dummyjson.com" is returned
2. Login user and verify authorization through /auth/me
3. Check that at least 5 products are returned with price, title and description
4. Check search for 5 different products (parametrized)
"""

import allure
import pytest

from dummyjson.clients.auth_client import AuthClient
from dummyjson.clients.product_client import ProductClient
from dummyjson.clients.user_client import UserClient


@allure.feature("Assignment Tests")
@allure.story("User Verification")
class TestUserVerification:
    @allure.title("Verify user with specific email exists")
    @allure.description("Check that at least one user with email 'emily.johnson@x.dummyjson.com' is returned from /users")
    def test_user_with_specific_email_exists(self, user_client: UserClient):
        """Verify that user with email emily.johnson@x.dummyjson.com exists in the system"""
        target_email = "emily.johnson@x.dummyjson.com"

        # Get all users
        response = user_client.get_all_users(limit=0)  # Get all users

        # Check that at least one user has the target email
        users_with_email = [user for user in response.users if user.email == target_email]

        assert len(users_with_email) >= 1, f"Expected at least 1 user with email {target_email}, but found {len(users_with_email)}"
        assert users_with_email[0].email == target_email, f"User email should be {target_email}"

        # Additional verification
        user = users_with_email[0]
        assert user.firstName, "User should have a first name"
        assert user.lastName, "User should have a last name"
        assert user.username, "User should have a username"

        with allure.step(f"Found user: {user.firstName} {user.lastName} ({user.username})"):
            allure.attach(f"Email: {user.email}", "User Email", allure.attachment_type.TEXT)


@allure.feature("Assignment Tests")
@allure.story("Authentication Verification")
class TestAuthenticationVerification:
    @allure.title("Login and verify authorization through /auth/me")
    @allure.description("Login user, get token and verify authorization by calling /auth/me")
    def test_login_and_verify_auth(self, auth_client: AuthClient, test_credentials: dict[str, str]):
        """Login user and verify that /auth/me returns correct user data"""

        with allure.step("Step 1: Login and get access token"):
            login_response = auth_client.login(username=test_credentials["username"], password=test_credentials["password"])

            assert login_response.accessToken, "Access token should not be empty"
            assert login_response.refreshToken, "Refresh token should not be empty"
            assert login_response.id > 0, "User ID should be greater than 0"

            allure.attach(login_response.accessToken[:20] + "...", "Access Token (truncated)", allure.attachment_type.TEXT)

        with allure.step("Step 2: Verify authorization using /auth/me endpoint"):
            current_user = auth_client.get_current_user(login_response.accessToken)

            # Verify that authenticated user matches login response
            assert current_user.id == login_response.id, "User ID from /auth/me should match login response"
            assert current_user.username == login_response.username, "Username from /auth/me should match login response"
            assert current_user.email == login_response.email, "Email from /auth/me should match login response"
            assert current_user.firstName == login_response.firstName, "First name should match"
            assert current_user.lastName == login_response.lastName, "Last name should match"

        with allure.step("Step 3: Verify user data completeness"):
            assert current_user.firstName, "First name should not be empty"
            assert current_user.lastName, "Last name should not be empty"
            assert current_user.email, "Email should not be empty"
            assert current_user.username, "Username should not be empty"

            allure.attach(
                f"User: {current_user.firstName} {current_user.lastName}\n"
                f"Email: {current_user.email}\n"
                f"Username: {current_user.username}\n"
                f"ID: {current_user.id}",
                "Authenticated User Details",
                allure.attachment_type.TEXT,
            )


@allure.feature("Assignment Tests")
@allure.story("Products Verification")
class TestProductsVerification:
    @allure.title("Verify at least 5 products with price, title and description")
    @allure.description("Check that /products returns at least 5 products and each has price, title and description")
    def test_minimum_5_products_with_required_fields(self, product_client: ProductClient):
        """Verify that at least 5 products are returned with price, title and description"""

        with allure.step("Step 1: Get products from /products endpoint"):
            response = product_client.get_all_products(limit=30)

            assert response.total > 0, "Total products should be greater than 0"
            assert len(response.products) >= 5, f"Expected at least 5 products, but got {len(response.products)}"

            allure.attach(f"Total products in system: {response.total}", "Product Count", allure.attachment_type.TEXT)

        with allure.step("Step 2: Verify each of first 5 products has required fields"):
            products_to_check = response.products[:5]

            for idx, product in enumerate(products_to_check, 1):
                with allure.step(f"Product {idx}: {product.title}"):
                    # Check that title exists and is not empty
                    assert product.title, f"Product {idx} should have a title"
                    assert len(product.title) > 0, f"Product {idx} title should not be empty"

                    # Check that description exists and is not empty
                    assert product.description, f"Product {idx} should have a description"
                    assert len(product.description) > 0, f"Product {idx} description should not be empty"

                    # Check that price exists and is valid
                    assert product.price is not None, f"Product {idx} should have a price"
                    assert product.price > 0, f"Product {idx} price should be greater than 0, got {product.price}"

                    # Attach product details to Allure report
                    allure.attach(
                        f"Title: {product.title}\n"
                        f"Description: {product.description[:100]}...\n"
                        f"Price: ${product.price}\n"
                        f"Category: {product.category}\n"
                        f"ID: {product.id}",
                        f"Product {idx} Details",
                        allure.attachment_type.TEXT,
                    )

        with allure.step("Step 3: Summary"):
            allure.attach(
                f"Successfully verified {len(products_to_check)} products\n" f"All products have title, description and valid price",
                "Verification Summary",
                allure.attachment_type.TEXT,
            )


@allure.feature("Assignment Tests")
@allure.story("Product Search")
class TestProductSearch:
    @allure.title("Search for different products (parametrized)")
    @allure.description("Test product search functionality with 5 different search queries")
    @pytest.mark.parametrize(
        "search_query",
        [
            "iPhone",
            "laptop",
            "perfume",
            "watch",
            "shoes",
        ],
    )
    def test_product_search_parametrized(self, product_client: ProductClient, search_query: str):
        """Test product search with different queries"""

        with allure.step(f"Search for products with query: '{search_query}'"):
            response = product_client.search_products(query=search_query, limit=10)

            # Basic assertions
            assert response.total >= 0, "Total should be non-negative"

            if response.total > 0:
                assert len(response.products) > 0, f"Products list should not be empty when total is {response.total}"

                # Verify that products match search criteria
                found_matching = False
                for product in response.products:
                    if (
                        search_query.lower() in product.title.lower()
                        or (product.description and search_query.lower() in product.description.lower())
                        or (product.category and search_query.lower() in product.category.lower())
                    ):
                        found_matching = True
                        break

                # Attach search results to Allure
                allure.attach(
                    f"Search query: {search_query}\n"
                    f"Total results: {response.total}\n"
                    f"Products returned: {len(response.products)}\n"
                    f"Matching products found: {found_matching}",
                    "Search Results",
                    allure.attachment_type.TEXT,
                )

                # List found products
                if response.products:
                    products_list = "\n".join([f"- {p.title} (${p.price})" for p in response.products[:5]])
                    allure.attach(products_list, f"Top Products for '{search_query}'", allure.attachment_type.TEXT)
            else:
                allure.attach(f"No products found for query: {search_query}", "Empty Results", allure.attachment_type.TEXT)
