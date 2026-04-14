from fastapi import APIRouter
from workflows.resolution_flow import process_resolution
from models.incident import ResolutionIncident

router = APIRouter()

@router.post("/resolution")
async def resolution(payload: ResolutionIncident):
    return await process_resolution(payload)