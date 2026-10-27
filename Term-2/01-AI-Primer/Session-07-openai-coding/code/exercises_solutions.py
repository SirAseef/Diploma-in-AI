"""Session 07 - Practice exercise solutions."""
# notebook: run-in-code-dir
import json
from llm_client import chat, get_client

client, MODEL = get_client()


def summarise(text):
    return chat(client, MODEL, "Summarise in one line.", text)


def classify_question(q):
    r = client.chat.completions.create(model=MODEL, temperature=0, response_format={"type": "json_object"},
                                       messages=[{"role": "system", "content": "Return JSON with keys topic and difficulty (1-5)."},
                                                 {"role": "user", "content": q}])
    data = json.loads(r.choices[0].message.content)
    if not (isinstance(data.get("difficulty"), int) and 1 <= data["difficulty"] <= 5):
        raise ValueError("bad difficulty")
    return data


def get_fee(course):
    return {"Diploma-AI": 45000, "Certificate-Web": 18000}[course]


def get_timing(course):
    return {"Diploma-AI": "Mon/Wed 6-8 pm", "Certificate-Web": "Sat 10-1"}[course]


TOOLS = {"get_fee": get_fee, "get_timing": get_timing}
SPECS = [{"type": "function", "function": {"name": n, "parameters": {"type": "object",
          "properties": {"course": {"type": "string"}}, "required": ["course"]}}} for n in TOOLS]


def route(question):
    msg = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": question}],
                                         tools=SPECS).choices[0].message
    call = msg.tool_calls[0]
    return call.function.name, TOOLS[call.function.name](**json.loads(call.function.arguments))


def batch_cost(n, tin, tout, price_in, price_out):
    return n * (tin * price_in + tout * price_out) / 1_000_000


if __name__ == "__main__":
    s = summarise("Search algorithms explore states; A star uses a heuristic to reach the goal faster than BFS.")
    print("ex1", s); assert isinstance(s, str) and s
    d = classify_question("Explain how BFS search works."); print("ex2", d); assert 1 <= d["difficulty"] <= 5
    r = route("What are the class timings for the Diploma AI?"); print("ex3", r); assert r[0] == "get_timing"
    c = batch_cost(500, 300, 150, 0.5, 1.5); print("ex4 cost $", c); assert abs(c - 0.1875) < 1e-9
    print("all exercises OK")
