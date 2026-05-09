import json
import os
import requests
import tomllib

#BASE: str = "http://127.0.0.1:8080"
BASE: str = "https://amethyst.aurillium.space"
PATH: str = "/api/devlog"
TOKEN: str = os.getenv("RECOVERY_TOKEN")
if TOKEN is None:
    raise ValueError("Set 'RECOVERY_TOKEN' environment variable.")

with open("devlog.toml", "rb") as f:
    data = tomllib.load(f)

for log in data["log"]:
    req: dict[str, str] = {
        "title": log["title"],
        "content": log["content"],
        "published": log["published"].isoformat()
    }
    resp = requests.post(BASE + PATH, json=req, headers={
        "Authorization": "Bearer " + TOKEN
    })
    print(resp.json())
