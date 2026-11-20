import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator
from app.models.document import DocumentStatus

class DocumentResponse(BaseModel):
    """Pydantic schema representing the document details returned in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    filename: str
    content_type: str
    file_size: int
    status: DocumentStatus
    error_message: Optional[str] = None
    error_log: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def sync_error_fields(self) -> "DocumentResponse":
        if self.error_message and not self.error_log:
            self.error_log = self.error_message
        elif self.error_log and not self.error_message:
            self.error_message = self.error_log
        return self
