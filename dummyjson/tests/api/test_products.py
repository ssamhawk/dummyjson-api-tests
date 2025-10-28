import allure
import pytest

from dummyjson.clients.product_client import ProductClient


@allure.feature("Products API")
@allure.story("Get Products")
class TestGetProducts:
    @allure.title("Get all products with default pagination")
    @allure.description("Verify that API returns a list of products with correct pagination")
    def test_get_all_products(self, product_client: ProductClient):
        response = product_client.get_all_products()

        assert response.total > 0, "Total products should be greater than 0"
        assert response.limit == 30, "Default limit should be 30"
        assert response.skip == 0, "Default skip should be 0"
        assert len(response.products) > 0, "Products list should not be empty"
        assert len(response.products) <= 30, "Products list should not exceed limit"

    @allure.title("Get products with custom pagination")
    @allure.description("Verify that API respects custom limit and skip parameters")
    @pytest.mark.parametrize("limit,skip", [(10, 0), (5, 10), (20, 40)])
    def test_get_products_with_pagination(self, product_client: ProductClient, limit: int, skip: int):
        response = product_client.get_all_products(limit=limit, skip=skip)

        assert response.limit == limit, f"Limit should be {limit}"
        assert response.skip == skip, f"Skip should be {skip}"
        assert len(response.products) <= limit, "Products list should not exceed limit"

    @allure.title("Get single product by ID")
    @allure.description("Verify that API returns correct product by ID")
    def test_get_product_by_id(self, product_client: ProductClient):
        product_id = 1
        product = product_client.get_product_by_id(product_id)

        assert product.id == product_id, f"Product ID should be {product_id}"
        assert product.title, "Product title should not be empty"
        assert product.price > 0, "Product price should be greater than 0"
        assert product.category, "Product category should not be empty"


@allure.feature("Products API")
@allure.story("Search Products")
class TestSearchProducts:
    @allure.title("Search products by query")
    @allure.description("Verify that API returns products matching search query")
    @pytest.mark.parametrize("query", ["phone", "laptop", "perfume"])
    def test_search_products(self, product_client: ProductClient, query: str):
        response = product_client.search_products(query=query)

        assert response.total >= 0, "Total should be non-negative"
        if response.total > 0:
            assert len(response.products) > 0, "Products list should not be empty when total > 0"
            # Check that at least one product contains the search query in title or description
            found = any(query.lower() in product.title.lower() or query.lower() in product.description.lower() for product in response.products)
            assert found, f"At least one product should contain '{query}' in title or description"


@allure.feature("Products API")
@allure.story("Products by Category")
class TestProductsByCategory:
    @allure.title("Get all product categories")
    @allure.description("Verify that API returns list of available categories")
    def test_get_all_categories(self, product_client: ProductClient):
        categories = product_client.get_all_categories()

        assert len(categories) > 0, "Categories list should not be empty"
        assert isinstance(categories, list), "Categories should be a list"

    @allure.title("Get products by category")
    @allure.description("Verify that API returns products from specific category")
    def test_get_products_by_category(self, product_client: ProductClient):
        # Use a known category
        test_category = "beauty"

        response = product_client.get_products_by_category(test_category)

        assert response.total >= 0, "Total should be non-negative"
        if response.total > 0:
            assert len(response.products) > 0, "Products list should not be empty"


@allure.feature("Products API")
@allure.story("Manage Products")
class TestManageProducts:
    @allure.title("Add new product")
    @allure.description("Verify that new product can be added")
    def test_add_product(self, product_client: ProductClient):
        new_product = {"title": "Test Product", "description": "Test Description", "price": 99.99, "category": "test"}

        product = product_client.add_product(new_product)

        assert product.title == new_product["title"], "Product title should match"
        assert product.description == new_product["description"], "Product description should match"
        assert product.price == new_product["price"], "Product price should match"

    @allure.title("Update existing product")
    @allure.description("Verify that product can be updated")
    def test_update_product(self, product_client: ProductClient):
        product_id = 1
        updated_data = {"title": "Updated Product Title"}

        product = product_client.update_product(product_id, updated_data)

        assert product.id == product_id, f"Product ID should be {product_id}"
        assert product.title == updated_data["title"], "Product title should be updated"

    @allure.title("Delete product")
    @allure.description("Verify that product can be deleted")
    def test_delete_product(self, product_client: ProductClient):
        product_id = 1

        product = product_client.delete_product(product_id)

        assert product.id == product_id, f"Deleted product ID should be {product_id}"
        assert product.isDeleted is True, "Product should be marked as deleted"
