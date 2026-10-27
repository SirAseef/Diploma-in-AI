"""Tiny connection helper used by the course's MongoDB examples.

- If the environment variable MONGO_URI is set (e.g. "mongodb://localhost:27017" or an
  Atlas "mongodb+srv://..." string) and pymongo is installed, a REAL MongoDB server is used.
- Otherwise an in-memory fake server from `mongomock` is used, so every example runs on a
  laptop with no database installed (pip install mongomock).
The calling code is identical either way: client["db"]["collection"].find(...).
"""
import os


def get_client():
    uri = os.environ.get("MONGO_URI")
    if uri:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        return client
    import mongomock
    return mongomock.MongoClient()


def get_db(name="campus"):
    return get_client()[name]


def backend():
    return "MongoDB server (pymongo)" if os.environ.get("MONGO_URI") else "in-memory mongomock"
