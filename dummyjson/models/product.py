from datetime import datetime

from base.models.base_model import BaseModel


class Dimensions(BaseModel):
    """Product dimensions model"""

    width: float
    height: float
    depth: float


class Review(BaseModel):
    """Product review model"""

    rating: int
    comment: str
    date: datetime
    reviewerName: str
    reviewerEmail: str


class Meta(BaseModel):
    """Product metadata model"""

    createdAt: datetime
    updatedAt: datetime
    barcode: str
    qrCode: str


class Product(BaseModel):
    """Product model"""

    id: int
    title: str
    description: str | None = None
    category: str
    price: float
    discountPercentage: float | None = None
    rating: float | None = None
    stock: int | None = None
    tags: list[str] | None = None
    brand: str | None = None
    sku: str | None = None
    weight: float | None = None
    dimensions: Dimensions | None = None
    warrantyInformation: str | None = None
    shippingInformation: str | None = None
    availabilityStatus: str | None = None
    reviews: list[Review] | None = None
    returnPolicy: str | None = None
    minimumOrderQuantity: int | None = None
    meta: Meta | None = None
    thumbnail: str | None = None
    images: list[str] | None = None
    isDeleted: bool | None = None  # For delete responses


class ProductsResponse(BaseModel):
    """Products list response model with pagination"""

    products: list[Product]
    total: int
    skip: int
    limit: int
