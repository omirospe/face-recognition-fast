from pydantic import BaseModel
from datetime import datetime, timezone


class FaceDetectResponse(BaseModel):
    id: str
    details: str
    created_at: datetime = datetime.now(timezone.utc)
