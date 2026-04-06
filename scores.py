import json
import os

SCORES_FILE = "scores.json"

def load_scores():
    # If the file doesn't exist yet, return empty defaults
    if not os.path.exists(SCORES_FILE):
        return {"high_score": 0, "history": []}
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_score(new_score):
    data = load_scores()

    # Update high score if beaten
    if new_score > data["high_score"]:
        data["high_score"] = new_score

    # Add to history, keep only last 5
    data["history"].append(new_score)
    data["history"] = data["history"][-5:]

    with open(SCORES_FILE, "w") as f:
        json.dump(data, f)

def get_high_score():
    return load_scores()["high_score"]

def get_history():
    return load_scores()["history"]