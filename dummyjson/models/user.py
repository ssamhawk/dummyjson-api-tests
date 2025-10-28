from base.models.base_model import BaseModel


class Hair(BaseModel):
    """User hair information"""

    color: str
    type: str


class Coordinates(BaseModel):
    """Geographic coordinates"""

    lat: float
    lng: float


class Address(BaseModel):
    """User address information"""

    address: str
    city: str
    state: str | None = None
    stateCode: str | None = None
    postalCode: str
    coordinates: Coordinates
    country: str


class CompanyAddress(BaseModel):
    """Company address information"""

    address: str
    city: str
    state: str | None = None
    stateCode: str | None = None
    postalCode: str
    coordinates: Coordinates
    country: str


class Company(BaseModel):
    """User company information"""

    department: str
    name: str
    title: str
    address: CompanyAddress


class Bank(BaseModel):
    """User bank information"""

    cardExpire: str
    cardNumber: str
    cardType: str
    currency: str
    iban: str


class Crypto(BaseModel):
    """User cryptocurrency information"""

    coin: str
    wallet: str
    network: str


class User(BaseModel):
    """User model"""

    id: int
    firstName: str
    lastName: str
    maidenName: str
    age: int
    gender: str
    email: str
    phone: str
    username: str
    password: str
    birthDate: str
    image: str
    bloodGroup: str
    height: float
    weight: float
    eyeColor: str
    hair: Hair
    ip: str
    address: Address
    macAddress: str
    university: str
    bank: Bank
    company: Company
    ein: str
    ssn: str
    userAgent: str
    crypto: Crypto
    role: str


class UsersResponse(BaseModel):
    """Users list response model with pagination"""

    users: list[User]
    total: int
    skip: int
    limit: int
