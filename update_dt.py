import json
import subprocess


def get_dt(thumb_name: str) -> str:
    try:
        result = subprocess.run(
            " ".join(
                ["git", "log", "-1", "--format=%ci", f'"./imgs/{thumb_name}.webp"']
            ),
            capture_output=True,
            text=True,
            check=True,
            shell=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "Unknown"


with open("./database.json") as f:
    database: dict = json.load(f)

    for key, value in database.items():
        value["date"] = get_dt(value["thumb_name"])

    with open("./database.json", "w", encoding="utf8") as f:
        json.dump(database, f, indent=4, sort_keys=True, ensure_ascii=False)
