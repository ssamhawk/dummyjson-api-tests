from base.models.base_model import BaseModel


class LoginRequest(BaseModel):
    """Login request model"""

    username: str
    password: str
    expiresInMins: int = 60


class LoginResponse(BaseModel):
    """Login response model"""

    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request model"""

    refreshToken: str
    expiresInMins: int = 60


class RefreshTokenResponse(BaseModel):
    """Refresh token response model"""

    accessToken: str
    refreshToken: str
