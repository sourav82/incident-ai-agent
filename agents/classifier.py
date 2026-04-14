from services.openai_client import client
from agents.kb_retriever import search_kb

def format_kb_context(results, top_k=3):
    context_blocks = []

    for i, r in enumerate(results[:top_k], 1):
        content = r.get("content", "").strip()
        title = r.get("title", "No Title")
        score = r.get("score", 0)

        block = f"""
KB Article {i}:
Title: {title}
Relevance Score: {score:.2f}
Content:
{content}
"""
        context_blocks.append(block)

    return "\n".join(context_blocks)

def classify_incident(short_description, description):

    with open("prompts/classifier_prompt.txt") as f:
        template = f.read()

    kb_results = search_kb(description)
    if len(kb_results) > 0:
        kb_context = format_kb_context(kb_results)
    else:
        kb_context = ""    

    prompt = template.format(
        short_description=short_description,
        description=description,
        kb_context=kb_context
    )

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0   # IMPORTANT
    )

    output = res.choices[0].message.content.strip()

    if output not in ["Network-L2", "MBS-L2", "IBS-L2", "Database-L2", "Level-1"]:
        raise Exception("Invalid classification")

    return output