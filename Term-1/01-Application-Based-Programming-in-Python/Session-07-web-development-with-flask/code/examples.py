"""Session 07 - exercising the Flask app with the test client (no browser needed)."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Load the app and create a test client

# %%
from app import app
client = app.test_client()

# %% [markdown]
# ## Simple and dynamic routes

# %%
for url in ["/", "/square/7", "/search?q=python", "/square/abc"]:
    r = client.get(url)
    print(url, "->", r.status_code, r.get_data(as_text=True)[:60])

# %% [markdown]
# ## Templates

# %%
html = client.get("/courses").get_data(as_text=True)
print("<li>Python</li>" in html, "<li>MongoDB</li>" in html)

# %% [markdown]
# ## Form with GET and POST

# %%
print(client.get("/feedback").status_code)
r = client.post("/feedback", data={"name": "Sana"})
print("Thank you, Sana!" in r.get_data(as_text=True))
r = client.post("/feedback", data={"name": ""})
print("Name is required." in r.get_data(as_text=True))

# %% [markdown]
# ## JSON API

# %%
r = client.get("/api/courses")
print(r.status_code, r.content_type, r.get_json())
