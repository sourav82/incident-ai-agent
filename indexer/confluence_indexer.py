import os
import json
import logging
from datetime import datetime, timezone

from services.confluence import fetch_articles
from services.openai_client import client
from services.search_service import client as search_client
from services.chunker import chunk_text

STATE_FILE = "/tmp/indexer_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_run_time": None, "indexed_page_ids": []}

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# =========================
# Load last run time
# =========================
# def load_last_run_time():
#     if not os.path.exists(STATE_FILE):
#         return None

#     with open(STATE_FILE, "r") as f:
#         data = json.load(f)

#     return data.get("last_run_time")


# =========================
# Save last run time
# =========================
# def save_last_run_time(timestamp):
#     with open(STATE_FILE, "w") as f:
#         json.dump({"last_run_time": timestamp}, f)

def delete_article_chunks(article_id):
    if not article_id:
        return
    try:
        for deleted_id in article_id:
            clean_id = str(deleted_id).strip("{}'")

            docs_to_delete = [
                {"id": f"{clean_id}_{i}"} for i in range(10000)
            ]

            search_client.delete_documents(docs_to_delete)    
    #    search_client.delete_documents(
    #        [{"id": f"{article_id}_{i}"} for i in range(10000)]  # or use filter if supported
    #    )
    except Exception as e:
        logging.error(f"Delete failed for {article_id}: {e}")

# =========================
# Main Indexer
# =========================
def run_indexer():

    logging.info("Starting Confluence indexer...")

    state = load_state()

    last_run_time = state.get("last_run_time")

    if last_run_time:
        last_run_time = datetime.fromisoformat(last_run_time)
        logging.info(f"Last run time: {last_run_time}")
    else:
        logging.info("No previous run found. Full indexing.")

    articles = fetch_articles()

    # =========================
    # Detect deleted pages
    # =========================

    previous_ids = set(state.get("indexed_page_ids", []))
    current_ids = set([article["id"] for article in articles])

    deleted_ids = previous_ids - current_ids

    logging.info(f"Deleted article IDs: {deleted_ids}")

    delete_article_chunks(deleted_ids)


    all_documents = []

    for article in articles:

        last_updated_str = article.get("last_updated")

        if not last_updated_str:
            continue

        last_updated = datetime.fromisoformat(last_updated_str)

        if last_run_time and last_updated <= last_run_time:
            continue

        logging.info(f"Indexing article: {article['title']}")

        chunks = chunk_text(article["content"])

        for i, chunk in enumerate(chunks):
            try:
                emb = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=chunk
                )

                all_documents.append({
                    "id": f"{article['id']}_{i}",
                    "content": chunk,
                    "embedding": emb.data[0].embedding,
                    "title": article["title"],
                    "url": article["url"],
                })

            except Exception as e:
                logging.error(f"Embedding failed for chunk {i}: {e}")

    # =========================
    # Batch Upload
    # =========================
    BATCH_SIZE = 100

    for i in range(0, len(all_documents), BATCH_SIZE):
        batch = all_documents[i:i + BATCH_SIZE]

        try:
            search_client.upload_documents(batch)
            logging.info(f"Uploaded batch of {len(batch)} documents")
        except Exception as e:
            logging.error(f"Upload failed: {e}")

    # =========================
    # Save current run time
    # =========================
    now = datetime.now(timezone.utc).isoformat()
    #save_last_run_time(now)

    state["last_run_time"] = now
    state["indexed_page_ids"] = list(current_ids)
    save_state(state)

    logging.info("Indexer completed")