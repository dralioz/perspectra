"""Module for defining base response models."""

from pydantic import BaseModel, Field


class PerspectraResponseModel(BaseModel):
    """
    Base class for all response models.
    """

    is_background_removed: bool = Field(default=False, description="Indicates if the background was removed")
    is_image_wrapped: bool = Field(default=False, description="Indicates if the image was wrapped")
    error_message: str = Field(default="", description="Error message if any error occurred")
    result: bool = Field(default=False, description="Indicates if the operation was successful")
    duration: float = Field(default=0.0, description="Time taken to process the request in seconds")
    processed_image: str = Field(default="", description="Processed image in base64 encoded format")
