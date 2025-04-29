import requests
import json
from datetime import datetime, timezone

with open("./database.json", encoding="utf8") as f:
    database: dict = json.load(f)

url = "https://app.bilibili.com/x/v2/splash/brand/list?appkey=1d8b6e7d45233436&ts=0&sign=78a89e153cd6231a4a4d55013aa063ce"

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}
response = requests.request("GET", url, headers=headers, data=payload)

update = []

if response.ok:
    for poster in response.json()["data"]["list"]:
        poster_id = f"{poster['id']:04d}"
        poster_name = poster["thumb_name"]
        poster_hash = poster["thumb_hash"]
        poster_url = poster["thumb"]
        thumb_hash = database.get(poster_id, {}).get("thumb_hash", "")
        if poster.get("thumb_hash") != thumb_hash:
            dt = datetime.now(timezone.utc).strftime(r"%Y-%m-%d %H:%M:%S %z")
            update.append((poster_id, poster_name))
            database[poster_id] = dict(
                thumb_name=poster_name,
                thumb=poster_url,
                thumb_hash=poster_hash,
                date=dt,
            )
            with open(f"./imgs/{poster_name}.webp", "wb+") as f:
                f.write(
                    requests.request(
                        "GET", poster_url, headers=headers, data=payload
                    ).content
                )

if update:
    print(update[0][1], end="")
    with open("./database.json", mode="w", encoding="utf8") as f:
        json.dump(database, f, sort_keys=True, indent=4, ensure_ascii=False)
