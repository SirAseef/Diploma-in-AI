"""LLM client helper for Session 07 (original code).

get_client() returns (client, model):
- the real OpenAI client if OPENAI_API_KEY is set and the `openai` package is installed;
- otherwise an offline FakeClient with the same chat.completions.create(...) interface,
  so teaching code runs anywhere without a key or network.
"""
import json
import os
import re
from types import SimpleNamespace


def estimate_tokens(text):
    return max(1, round(len(text) / 4))


class FakeCompletions:
    """Deterministic rule-based stand-in. It is NOT a language model."""

    def create(self, model, messages, temperature=0, response_format=None, tools=None, **kw):
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        last = messages[-1]
        user = last.get("content") or ""
        tool_calls = None
        if last["role"] == "tool":
            content = f"The answer is: {last['content']}"
        elif tools:
            call = self._pick_tool(user, tools)
            if call:
                tool_calls = [SimpleNamespace(id="call_1", type="function",
                                              function=SimpleNamespace(name=call[0], arguments=json.dumps(call[1])))]
                content = None
            else:
                content = "No tool needed."
        elif response_format and response_format.get("type") == "json_object":
            content = json.dumps(self._json_reply(system, user))
        else:
            content = self._text_reply(user)
        prompt_t = sum(estimate_tokens(m.get("content") or "") for m in messages)
        comp_t = estimate_tokens(content or "")
        msg = SimpleNamespace(role="assistant", content=content, tool_calls=tool_calls)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg, finish_reason="stop")],
                               usage=SimpleNamespace(prompt_tokens=prompt_t, completion_tokens=comp_t,
                                                     total_tokens=prompt_t + comp_t), model=model)

    @staticmethod
    def _text_reply(user):
        u = user.lower()
        canned = {"machine learning": "Machine learning lets computers learn patterns from data instead of hand-written rules.",
                  "bfs": "BFS explores a graph level by level using a queue.",
                  "dfs": "DFS follows one branch as deep as possible using a stack, then backtracks."}
        for k, v in canned.items():
            if k in u:
                return v
        words = re.findall(r"\w+", user)
        return "Summary: " + " ".join(words[:12]) + ("..." if len(words) > 12 else "")

    @staticmethod
    def _json_reply(system, user):
        keys = re.findall(r"\b(sentiment|score|answer|source|topic|difficulty)\b", system.lower())
        u = user.lower()
        out = {}
        for k in dict.fromkeys(keys):
            if k == "sentiment":
                out[k] = "positive" if re.search(r"excellent|good|great|love", u) else (
                    "negative" if re.search(r"bad|poor|boring|hate", u) else "neutral")
            elif k == "score":
                out[k] = 0.9 if out.get("sentiment") == "positive" else 0.1 if out.get("sentiment") == "negative" else 0.5
            elif k == "answer":
                m = re.search(r"context \[[^\]]*\]: (.*?)\nquestion", user, re.S | re.I)
                out[k] = m.group(1).strip() if m else "I don't know."
            elif k == "source":
                m = re.search(r"context \[([^\]]*)\]", user, re.I)
                out[k] = m.group(1) if m else None
            elif k == "topic":
                out[k] = "search" if "search" in u or "bfs" in u else "machine learning" if "learn" in u else "general"
            elif k == "difficulty":
                out[k] = 2 if len(u) < 60 else 4
        return out

    @staticmethod
    def _pick_tool(user, tools):
        u = user.lower()
        names = [t["function"]["name"] for t in tools]
        course = "Diploma-AI" if "ai" in u.split() or "diploma" in u else "Certificate-Web"
        if "fee" in u and "get_fee" in names:
            return "get_fee", {"course": course}
        if ("timing" in u or "time" in u) and "get_timing" in names:
            return "get_timing", {"course": course}
        return None


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())
        self.is_fake = True


def get_client():
    model = os.environ.get("OPENAI_MODEL", "your-model-name")
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            return OpenAI(), model
        except ImportError:
            pass
    return FakeClient(), model


def chat(client, model, system, user, temperature=0):
    r = client.chat.completions.create(model=model, temperature=temperature,
                                       messages=[{"role": "system", "content": system},
                                                 {"role": "user", "content": user}])
    return r.choices[0].message.content
