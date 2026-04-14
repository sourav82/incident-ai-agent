from services.openai_client import client
import json

def decide_action(classification, kb_results):

    with open("prompts/decision_prompt.txt") as f:
        template = f.read()

    prompt = template.format(
        classification=classification,
        kb_results=kb_results
    )

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    output = res.choices[0].message.content.strip()

    if output not in ["USE_KB", "OUTLIER"]:
        raise Exception("Invalid decision")

    return output

def detect_outlier(text):

    with open("prompts/outlier_prompt.txt") as f:
        template = f.read()

    prompt = template.format(incident_text=text)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(res.choices[0].message.content)