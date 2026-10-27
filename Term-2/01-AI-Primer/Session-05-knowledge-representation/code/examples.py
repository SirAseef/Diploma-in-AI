"""Session 05 - Knowledge Representation: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - a triple store

# %%
from kb import Frame, SemanticNet, TripleStore, forward_chain, is_subclass

kb = TripleStore()
kb.add("Karachi", "located_in", "Sindh"); kb.add("Hyderabad", "located_in", "Sindh")
kb.add("Sindh", "located_in", "Pakistan"); kb.add("Lahore", "located_in", "Punjab")
kb.add("Punjab", "located_in", "Pakistan"); kb.add("Karachi", "population_millions", 20)
print(kb.query(None, "located_in", "Sindh"))
print("Karachi population:", kb.one("Karachi", "population_millions"))

# %% [markdown]
# ## Example 2 - transitive queries

# %%
print("Karachi is inside:", kb.transitive("Karachi", "located_in"))

# %% [markdown]
# ## Example 3 - semantic network with inheritance and exceptions

# %%
net = SemanticNet()
net.add_isa("bird", "animal"); net.add_isa("sparrow", "bird"); net.add_isa("penguin", "bird")
net.set("animal", "has_skin", True); net.set("bird", "can_fly", True); net.set("penguin", "can_fly", False)
for n in ["sparrow", "penguin"]:
    print(n, "can_fly:", net.get(n, "can_fly"), "has_skin:", net.get(n, "has_skin"))

# %% [markdown]
# ## Example 4 - frames with slots and defaults

# %%
course = Frame("Course", hours=36, mode="on-campus")
ai_primer = Frame("AI Primer", parent=course, hours=14)
print(ai_primer.name, ai_primer["hours"], ai_primer["mode"])

# %% [markdown]
# ## Example 5 - production rules with forward chaining

# %%
rules = [({"fever", "cough"}, "flu_suspected"), ({"flu_suspected", "short_breath"}, "see_doctor")]
print(sorted(forward_chain({"fever", "cough", "short_breath"}, rules)))

# %% [markdown]
# ## Example 6 - a tiny ontology check

# %%
onto = {"Student": "Person", "Faculty": "Person", "Person": "Thing"}
print("Student subclass of Thing?", is_subclass("Student", "Thing", onto))
print("Student subclass of Faculty?", is_subclass("Student", "Faculty", onto))
