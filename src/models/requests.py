"""Request models for the application."""

from pydantic import BaseModel, Field


class PerspectraRequestModel(BaseModel):
    """
    Base class for all request models.
    """

    session_id: str = Field(default="", description="Session identifier")
    guid: str = Field(default="", description="Global unique identifier")
    channel_id: str = Field(default="", description="Channel identifier")
    image: bytes = Field(default=b"", description="Image data in bytes")
