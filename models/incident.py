from pydantic import BaseModel

class Incident(BaseModel):
    incident_number: str
    short_description: str
    description: str
    sys_id: str

class ResolutionIncident(Incident):
    close_notes: str
    work_notes: str
    resolution_code: str
    resolved_by: str
