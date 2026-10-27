"""Session 07 - OpenAI Coding in Python: worked examples (offline fake client unless OPENAI_API_KEY is set)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - a first chat completion

# %%
import json
import time
from llm_client import estimate_tokens, get_client

client, MODEL = get_client()
print("using fake offline client:", getattr(client, "is_fake", False))
r = client.chat.completions.create(model=MODEL, temperature=0, messages=[
    {"role": "system", "content": "You are a concise tutor."},
    {"role": "user", "content": "Define machine learning in one sentence."}])
print(r.choices[0].message.content)
print("tokens used:", r.usage.total_tokens)

# %% [markdown]
# ## Example 2 - multi-turn chat keeps history

# %%
history = [{"role": "system", "content": "You are a helpful tutor."}]
for q in ["What is BFS?", "And DFS?"]:
    history.append({"role": "user", "content": q})
    reply = client.chat.completions.create(model=MODEL, messages=history).choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    print("Q:", q, "\nA:", reply)
print("messages in history:", len(history))

# %% [markdown]
# ## Example 3 - structured JSON output

# %%
r = client.chat.completions.create(model=MODEL, temperature=0, response_format={"type": "json_object"}, messages=[
    {"role": "system", "content": "Reply as JSON with keys sentiment and score."},
    {"role": "user", "content": "The lab session was excellent!"}])
data = json.loads(r.choices[0].message.content)
print(data)
assert {"sentiment", "score"} <= set(data)

# %% [markdown]
# ## Example 4 - tool (function) calling

# %%
FEES = {"Diploma-AI": 45000, "Certificate-Web": 18000}

def get_fee(course):
    return FEES.get(course, "unknown")

tools = [{"type": "function", "function": {
    "name": "get_fee", "description": "Monthly fee in PKR for a course",
    "parameters": {"type": "object", "properties": {"course": {"type": "string"}}, "required": ["course"]}}}]
msgs = [{"role": "user", "content": "What is the fee for the Diploma AI?"}]
msg = client.chat.completions.create(model=MODEL, messages=msgs, tools=tools).choices[0].message
if msg.tool_calls:
    call = msg.tool_calls[0]
    args = json.loads(call.function.arguments)
    result = get_fee(**args)
    print("model asked for", call.function.name, args, "->", result)
    msgs += [{"role": "assistant", "content": None, "tool_calls": [
                 {"id": call.id, "type": "function",
                  "function": {"name": call.function.name, "arguments": call.function.arguments}}]},
             {"role": "tool", "tool_call_id": call.id, "content": str(result)}]
    print(client.chat.completions.create(model=MODEL, messages=msgs, tools=tools).choices[0].message.content)

# %% [markdown]
# ## Example 5 - estimating tokens and cost

# %%
prompt = "Explain the difference between supervised and unsupervised learning with two examples each."
PRICE_IN_PER_MILLION = 0.50   # illustrative number only - check the provider's current price list
tokens = estimate_tokens(prompt)
print("approx tokens:", tokens, "approx cost for 10,000 such prompts: $",
      round(10_000 * tokens / 1_000_000 * PRICE_IN_PER_MILLION, 4))

# %% [markdown]
# ## Example 6 - retries with exponential back-off

# %%
class TransientError(Exception):
    pass

attempts = {"n": 0}

def flaky_call():
    attempts["n"] += 1
    if attempts["n"] < 3:
        raise TransientError("rate limited")
    return "success on attempt %d" % attempts["n"]

def with_retry(fn, tries=4, base=0.01):
    for i in range(tries):
        try:
            return fn()
        except TransientError as e:
            print("retry", i + 1, "after error:", e)
            time.sleep(base * 2 ** i)
    raise RuntimeError("gave up")

print(with_retry(flaky_call))
