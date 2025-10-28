from pydantic import BaseModel as PydanticBaseModel, ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model for all API response models with common configuration"""

    model_config = ConfigDict(
        extra="ignore",  # Ignore extra fields in API responses
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,  # Validate field assignments after object creation
    )
