from agents.classifier import classify_incident
from agents.kb_retriever import retrieve_kb
from agents.decision import decide_action
from services.servicenow import update_notes
from services.email import send_outlier_email
from agents.decision import detect_outlier


async def process_incident(incident, has_attachments=False):

    text = incident.short_description + " " + incident.description

    classification = await classify_incident(incident, has_attachments)

    kb_results = retrieve_kb(text)

    #outlier_result = detect_outlier(text)

    # if outlier_result["outlier"]:
    #     send_outlier_email(None, incident.incident_number, incident.description)
    #     return "OUTLIER_DETECTED"

    decision = decide_action(classification, kb_results)

    if decision == "USE_KB":
        update_notes(incident.sys_id, classification, kb_results[0])
    else:
        update_notes(incident.sys_id, classification)
        send_outlier_email(None, incident.incident_number, incident.description)

    return decision