from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    status: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Health check message")


class HealthResponseModel(BaseModel):
    message: str = Field(..., description="Health check response message")
