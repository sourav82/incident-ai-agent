import json
from services.openai_client import client
from services.search_service import vector_search
import logging

def truncate_text(text, max_chars=6000):
    return text[:max_chars]

def search_kb(text):
    safe_text = truncate_text(text)
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=safe_text
    ).data[0].embedding

    results = vector_search(embedding)
    filtered = [r for r in results if r.get("score", 0) > 0.7]
    return filtered

def retrieve_kb(text):

    safe_text = truncate_text(text)
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=safe_text
    ).data[0].embedding

    results = vector_search(embedding)

    validated_results = []

    for r in results:

        with open("prompts/kb_relevance_prompt.txt") as f:
            template = f.read()

        prompt = template.format(
            incident_text=text,
            title=r["title"],
            content=r["content"]
        )

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        raw = res.choices[0].message.content
        print(f"{raw}")
        try:
            decision = json.loads(raw)
            logging.info(f"Decision json: {decision}")
        except json.JSONDecodeError:
            decision = {"relevant": False, "confidence": 0.0}

        #decision = json.loads(res.choices[0].message.content)

        if decision["relevant"] and decision["confidence"] > 0.65:
            validated_results.append(r)

    return validated_results