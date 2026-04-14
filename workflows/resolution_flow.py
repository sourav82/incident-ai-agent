from agents.kb_retriever import retrieve_kb
from agents.kb_author import create_kb_article
from services.confluence import create_page, update_page
from agents.kb_update_decision import decide_kb_update
import logging
import json
from urllib.parse import urlparse, parse_qs

async def process_resolution(incident):

    logging.info(f"Resolved data: {json.dumps(incident.dict() if hasattr(incident, 'dict') else incident)}")

    text = incident.description + " " + incident.close_notes

    kb_results = retrieve_kb(text)

    # CASE 1: No KB exists → Create new
    if not kb_results:
        article = create_kb_article(text, incident.close_notes)
        create_page(incident.incident_number, incident.short_description,  article)
        return "CREATED_NEW_KB"

    # CASE 2: KB exists → Decide update or new
    existing_kb = kb_results[0]

    decision = decide_kb_update(
        incident_text=text,
        kb_content=existing_kb["content"]
    )

    if decision == "UPDATE_EXISTING":
        parsed = urlparse(existing_kb["url"])
        params = parse_qs(parsed.query)

        page_id = params.get("pageId", [None])[0]

        print(page_id)
        update_page(page_id, incident.incident_number)
        return "UPDATED_EXISTING_KB"

    else:
        article = create_kb_article(text, incident.close_notes)
        create_page(incident.incident_number, incident.short_description,  article)
        return "CREATED_NEW_KB"