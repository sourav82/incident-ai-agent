import requests
from requests.auth import HTTPBasicAuth
from app.config import CONFLUENCE_BASE_URL, CONFLUENCE_API_TOKEN, CONFLUENCE_EMAIL, CONFLUENCE_SPACE_KEY


HEADERS = {
    "Content-Type": "application/json"
}


# =========================
# 1️⃣ FETCH ARTICLES (Indexer)
# =========================
# def fetch_articles():

#     url = f"{CONFLUENCE_BASE_URL}/rest/api/content"

#     params = {
#         "limit": 50,
#         "expand": "body.storage"
#     }

#     response = requests.get(
#         url,
#         headers=HEADERS,
#         auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
#         params=params
#     )

#     data = response.json()

#     articles = []

#     for page in data.get("results", []):

#         articles.append({
#             "id": page["id"],
#             "title": page["title"],
#             "content": page["body"]["storage"]["value"],
#             "url": f"{CONFLUENCE_BASE_URL}/pages/viewpage.action?pageId={page['id']}"
#         })

#     return articles

def fetch_articles():

    url = f"{CONFLUENCE_BASE_URL}/rest/api/content"

    params = {
        "spaceKey": CONFLUENCE_SPACE_KEY,
        "limit": 50,
        "expand": "body.storage,version"
    }

    response = requests.get(
        url,
        headers=HEADERS,
        auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
        params=params
    )

    data = response.json()

    articles = []

    for page in data.get("results", []):

        articles.append({
            "id": page["id"],
            "title": page["title"],
            "content": page["body"]["storage"]["value"],
            "url": f"{CONFLUENCE_BASE_URL}/pages/viewpage.action?pageId={page['id']}",
            "last_updated": page["version"]["when"]
        })

    return articles

# =========================
# 2️⃣ CREATE KB PAGE
# =========================
def create_page(incident_number, shor_description, article_content):

    url = f"{CONFLUENCE_BASE_URL}/rest/api/content"

    title = incident_number + ": " + shor_description

    payload = {
        "type": "page",
        "title": title,
        "space": {
            "key": CONFLUENCE_SPACE_KEY   # 🔥 change to your space
        },
        "body": {
            "storage": {
                "value": article_content,
                "representation": "storage"
            }
        }
    }

    response = requests.post(
        url,
        headers=HEADERS,
        auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
        json=payload
    )

    return response.json()


# =========================
# 3️⃣ UPDATE EXISTING PAGE
# =========================
def update_page(page_id, incident_number):

    # Step 1: Get existing content
    get_url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage,version"

    response = requests.get(
        get_url,
        headers=HEADERS,
        auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)
    )

    page = response.json()

    current_content = page["body"]["storage"]["value"]
    version = page["version"]["number"]

    # Append incident reference
    updated_content = current_content + f"<p>Related Incident: {incident_number}</p>"

    # Step 2: Update page
    update_url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"

    payload = {
        "id": page_id,
        "type": "page",
        "title": page["title"],
        "version": {
            "number": version + 1
        },
        "body": {
            "storage": {
                "value": updated_content,
                "representation": "storage"
            }
        }
    }

    response = requests.put(
        update_url,
        headers=HEADERS,
        auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
        json=payload
    )

    return response.json()