from fastapi import APIRouter
from workflows.incident_flow import process_incident
from models.incident import Incident

router = APIRouter()

@router.post("/incident")
async def incident(payload: Incident):
    return await process_incident(payload)