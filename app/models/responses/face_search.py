from pydantic import BaseModel
from datetime import datetime,timezone
from typing import List

class FaceSearchResponse(BaseModel):
    id: str
    completed_at: datetime = datetime.now(timezone.utc)
