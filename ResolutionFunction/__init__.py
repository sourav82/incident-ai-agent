import azure.functions as func
import json
from workflows.resolution_flow import process_resolution
from models.incident import ResolutionIncident
import logging
import re




async def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        raw_body = req.get_body().decode("utf-8", errors="ignore")

        sanitized = re.sub(r'[\x00-\x1F]+', ' ', raw_body)

        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]+', ' ', sanitized)

        body = json.loads(sanitized) #req.get_json()

        logging.info(f"Body: {json.dumps(body)}")

        incident = ResolutionIncident(**body)

        logging.info(f"Result type: {type(incident)}")

        result = await process_resolution(incident)

        logging.info(f"Result type: {type(result)}")

        return func.HttpResponse(
            json.dumps({"status": "ok", "result": result}),
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        return func.HttpResponse(
            str(e),
            status_code=500
        )