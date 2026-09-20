import json
import os
from datetime import datetime

from scoring import (
    calculate_score,
    determine_level,
    determine_recommendation
)


USER = "demo_hr"

DATABASE_FILE = f"database_{USER}.json"
HISTORY_FILE = f"history_{USER}.json"


with open(DATABASE_FILE, "r", encoding="utf-8") as file:
    candidates = json.load(file)


if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    if history:
        print(f"{HISTORY_FILE} already contains evaluation history.")
        print("No changes were made.")
        exit()


history = []

date = datetime.now().strftime("%Y-%m-%d %H:%M")


for candidate in candidates:

    score = calculate_score(
        candidate["experienta"],
        candidate["performanta"],
        candidate["certificari"]
    )

    level = determine_level(score)

    recommendation = determine_recommendation(score)

    history.append({
        "nume": candidate["nume"],
        "scor": score,
        "nivel": level,
        "recomandare": recommendation,
        "data": date
    })


with open(HISTORY_FILE, "w", encoding="utf-8") as file:
    json.dump(history, file, indent=4)


print(f"Created {HISTORY_FILE}")
print(f"Initial evaluations created: {len(history)}")

for evaluation in history:
    print(
        f"{evaluation['nume']}: "
        f"{evaluation['scor']}/100 - "
        f"{evaluation['nivel']}"
    )