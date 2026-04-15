from pydantic import BaseModel
from typing import List, Optional

class Attachment(BaseModel):
    file_name: str
    content_type: str
    data: str  # base64


class Incident(BaseModel):
    incident_number: str
    short_description: str
    description: str
    sys_id: str
    attachments: Optional[List[Attachment]] = []  # ✅ NEW


class ResolutionIncident(Incident):
    close_notes: str
    work_notes: str
    resolution_code: str
    resolved_by: str