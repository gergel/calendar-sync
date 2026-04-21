import json
import os

STATE_FILE = "/data/state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "sync_token": None,
            "imported_ids": [],
            "run_count": 0
        }

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
