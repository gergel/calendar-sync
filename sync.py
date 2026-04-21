from google import get_events
from notion import upsert_event, delete_event, get_existing_ids
import json
import os

STATE_FILE = "sync_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def run_sync():
    state = load_state()
    sync_token = state.get("sync_token")

    data = get_events(sync_token)

    events = data["items"]
    next_sync_token = data.get("nextSyncToken")

    existing_ids = get_existing_ids()

    for e in events:
        event_id = e["id"]

        if e.get("status") == "cancelled":
            delete_event(event_id)
            continue

        upsert_event(e, existing_ids)

    if next_sync_token:
        state["sync_token"] = next_sync_token
        save_state(state)
