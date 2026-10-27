"""Session 04 - Search as a Universal Problem-Solving Agent: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - BFS on the water-jug problem

# %%
from problems import EightPuzzle, WaterJug
from search import (COORDS, ROADS, RouteProblem, astar, breadth_first, depth_first,
                    greedy, manhattan, misplaced, uniform_cost)

node = breadth_first(WaterJug())
print("plan:", node.path_actions())
print("states:", node.path_states())

# %% [markdown]
# ## Example 2 - a road map as a problem

# %%
route = RouteProblem("Karachi", "Islamabad", ROADS, COORDS)
print("neighbours of Multan:", route.actions("Multan"))

# %% [markdown]
# ## Example 3 - UCS finds the cheapest route

# %%
stats = {}
node = uniform_cost(route, stats)
print(node.path_states(), node.path_cost, "km | expanded:", stats["expanded"])

# %% [markdown]
# ## Example 4 - A* with a straight-line heuristic

# %%
stats = {}
node = astar(route, h=route.h, stats=stats)
print(node.path_states(), node.path_cost, "km | expanded:", stats["expanded"])

# %% [markdown]
# ## Example 5 - DFS is not optimal

# %%
node = depth_first(route)
print(node.path_states(), node.path_cost, "km")

# %% [markdown]
# ## Example 6 - A* on the 8-puzzle: misplaced vs Manhattan

# %%
start = (7, 2, 4, 5, 0, 6, 8, 3, 1)
for h in (misplaced, manhattan):
    stats = {}
    node = astar(EightPuzzle(start), h=h, stats=stats)
    print(f"{h.__name__:10s} moves={len(node.path_actions())} expanded={stats['expanded']}")
print("greedy (Manhattan) moves:", len(greedy(EightPuzzle(start), manhattan).path_actions()))
