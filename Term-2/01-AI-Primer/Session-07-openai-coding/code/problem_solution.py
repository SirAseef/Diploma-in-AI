"""Session 07 - Real-life problem: grounded admissions FAQ assistant returning JSON."""
# notebook: run-in-code-dir
import json
import re
from llm_client import get_client

SNIPPETS = {
    "fees": "The Diploma in AI monthly fee is PKR 45,000 and the admission fee is PKR 10,000.",
    "timings": "Diploma in AI classes run Monday and Wednesday from 6 pm to 8 pm on campus.",
    "eligibility": "Eligibility for the Diploma in AI is intermediate (HSC) or A-levels with mathematics.",
}


STOP = {"is", "the", "a", "an", "for", "in", "of", "and", "what", "when", "do", "does", "there", "to", "on", "from"}


def words(text):
    return set(re.findall(r"\w+", text.lower())) - STOP


def retrieve(question):
    q = words(question)
    scored = [(len(q & words(t)), k) for k, t in SNIPPETS.items()]
    best_score, best = max(scored)
    return (best, SNIPPETS[best]) if best_score >= 2 else (None, None)


def ask(client, model, question):
    key, text = retrieve(question)
    if key is None:
        return {"answer": "Please contact the front desk.", "source": None}
    r = client.chat.completions.create(
        model=model, temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": "Answer ONLY from the context. Reply as JSON with keys answer and source."},
                  {"role": "user", "content": f"Context [{key}]: {text}\nQuestion: {question}"}])
    data = json.loads(r.choices[0].message.content)
    if set(data) != {"answer", "source"}:
        raise ValueError(f"unexpected keys {set(data)}")
    return data


if __name__ == "__main__":
    client, model = get_client()
    qs = ["What is the monthly fee for the Diploma in AI?", "When do Diploma in AI classes run?",
          "Is there a hostel for girls?"]
    answers = [ask(client, model, q) for q in qs]
    for q, a in zip(qs, answers):
        print(q, "->", a)
    if getattr(client, "is_fake", False):
        assert answers[0]["source"] == "fees" and "45,000" in answers[0]["answer"]
        assert answers[1]["source"] == "timings"
    assert answers[2]["source"] is None
    print("OK")
