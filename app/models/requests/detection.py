from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from fastapi import UploadFile


class FaceDetectionRequest(BaseModel):
    metadata: Optional[dict] = None
    callback_url: str
    photo_url: HttpUrl = Field(..., description="URL of the photo to analyze")
    id: str = Field(..., min_length=1,
                    description="Unique identifier for the request")

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {"source": "mobile_app"},
                "photo_url": "https://example.com/photo.jpg",
                "id": "request_123"
            }
        }


class AddFaceToCollection(BaseModel):
    file: UploadFile = None
    id: str = Field(..., min_length=1,
                    description="Unique identifier for the request")
