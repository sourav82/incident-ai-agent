from services.openai_client import client

def decide_kb_update(incident_text, kb_content):

    with open("prompts/kb_update_decision.txt") as f:
        template = f.read()

    prompt = template.format(
        incident_text=incident_text,
        kb_content=kb_content
    )

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()