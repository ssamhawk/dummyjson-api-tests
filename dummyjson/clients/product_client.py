from typing import Any

from base.api.api_client import APIClient
from dummyjson.models.product import Product, ProductsResponse


class ProductClient:
    """Client for DummyJSON Products API"""

    def __init__(self, api_client: APIClient):
        self.api = api_client

    def get_all_products(self, limit: int = 30, skip: int = 0) -> ProductsResponse:
        """Get all products with pagination"""
        response = self.api.get(f"/products?limit={limit}&skip={skip}")
        return ProductsResponse.model_validate(response.json())

    def get_product_by_id(self, product_id: int) -> Product:
        """Get a single product by ID"""
        response = self.api.get(f"/products/{product_id}")
        return Product.model_validate(response.json())

    def search_products(self, query: str, limit: int = 30, skip: int = 0) -> ProductsResponse:
        """Search products by query"""
        response = self.api.get(f"/products/search?q={query}&limit={limit}&skip={skip}")
        return ProductsResponse.model_validate(response.json())

    def get_products_by_category(self, category: str, limit: int = 30, skip: int = 0) -> ProductsResponse:
        """Get products by category"""
        response = self.api.get(f"/products/category/{category}?limit={limit}&skip={skip}")
        return ProductsResponse.model_validate(response.json())

    def get_all_categories(self) -> list[Any]:
        """Get all product categories"""
        response = self.api.get("/products/categories")
        categories = response.json()
        # Extract slug if categories are returned as objects
        if categories and isinstance(categories[0], dict):
            return [cat.get("slug", cat.get("name", "")) for cat in categories]
        return categories

    def add_product(self, product_data: dict[str, Any]) -> Product:
        """Add a new product"""
        response = self.api.post("/products/add", json=product_data)
        return Product.model_validate(response.json())

    def update_product(self, product_id: int, product_data: dict[str, Any]) -> Product:
        """Update a product"""
        response = self.api.put(f"/products/{product_id}", json=product_data)
        return Product.model_validate(response.json())

    def delete_product(self, product_id: int) -> Product:
        """Delete a product"""
        response = self.api.delete(f"/products/{product_id}")
        return Product.model_validate(response.json())
