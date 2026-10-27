"""Session 02 - Advanced Recommender Systems: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - a synthetic ratings matrix

# %%
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recsys import factorise, make_ratings, precision_at_k, rmse, split_mask, user_knn_predict

R_true, R, mask = make_ratings(n_users=60, n_items=25, k=3, density=0.3)
print("shape:", R.shape, "observed ratings:", int(mask.sum()), f"({mask.mean():.0%})")

# %% [markdown]
# ## Example 2 - popularity baseline

# %%
avg = np.nanmean(np.where(mask, R, np.nan), axis=0)
counts = mask.sum(0)
score = np.where(counts >= 5, avg, 0)
print("top-5 popular items:", np.argsort(-score)[:5], "avg:", np.sort(score)[::-1][:5].round(2))

# %% [markdown]
# ## Example 3 - content-based with TF-IDF

# %%
descriptions = ["family drama joint family wedding", "romance love story college", "thriller crime police karachi",
                "family wedding comedy", "historical drama mughal empire", "romance wedding family"]
tfidf = TfidfVectorizer().fit_transform(descriptions)
sim = cosine_similarity(tfidf)
print("items most like item 0:", np.argsort(-sim[0])[1:4], sim[0].round(2))

# %% [markdown]
# ## Example 4 - user-based collaborative filtering

# %%
train, test = split_mask(mask)
R_train = np.where(train, R, 0)
u, i = np.argwhere(test)[0]
print(f"user {u}, item {i}: predicted {user_knn_predict(R_train, train, u, i):.2f}, actual {R[u, i]:.0f}")

# %% [markdown]
# ## Example 5 - matrix factorisation by gradient descent

# %%
P, Q, B = factorise(R_train, train, k=3, epochs=300)
R_hat = B + P @ Q.T
print("P:", P.shape, "Q:", Q.shape)

# %% [markdown]
# ## Example 6 - evaluate: RMSE and precision@k

# %%
baseline = np.full_like(R, R_train[train].mean(), dtype=float)
print("RMSE global mean:", round(rmse(R, baseline, test), 3))
print("RMSE matrix factorisation:", round(rmse(R, R_hat, test), 3))
print("precision@5 MF:", round(precision_at_k(R_hat, R_true, train, 5), 3),
      "| popularity:", round(precision_at_k(np.tile(score, (R.shape[0], 1)), R_true, train, 5), 3))
