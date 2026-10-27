"""Session 11 - Practice exercise solutions."""
# notebook: run-in-code-dir
import re
from urllib.parse import quote_plus, unquote_plus
from atlas_helpers import describe_uri

if __name__ == "__main__":
    enc = quote_plus("Karachi#2026!")
    assert enc == "Karachi%232026%21" and unquote_plus(enc) == "Karachi#2026!"

    info = describe_uri("mongodb+srv://u:p@cluster9.xyz.mongodb.net/shop?retryWrites=true&w=majority")
    assert info["db"] == "shop" and info["options"] == {"retryWrites": "true", "w": "majority"}

    def mask(uri):
        return re.sub(r"(://[^:/@]+):[^@]+@", r"\1:****@", uri)
    assert mask("mongodb+srv://ali:secret@c.mongodb.net/") == "mongodb+srv://ali:****@c.mongodb.net/"

    steps = ["Database Access -> add user with role 'read' on campus",
             "Network Access -> add the teammate's public IP (/32)",
             "Share the connection string through a secure channel; teammate stores it in MONGO_URI"]
    print("\n".join(steps))
    print("All exercise checks passed")
