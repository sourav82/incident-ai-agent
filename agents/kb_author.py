from services.openai_client import client

def create_kb_article(incident_text, engineer_notes):

    with open("prompts/kb_author_prompt.txt") as f:
        template = f.read()

    prompt = template.format(
        incident_text=incident_text,
        engineer_notes=engineer_notes
    )

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return res.choices[0].message.content