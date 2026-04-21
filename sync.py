from google_api import get_events
from notion_api import (
    create_event,
    update_event,
    archive_event,
    build_indexes,
    build_event_key,
)
from state import load_state, save_state


def run_sync():
    state = load_state()
    sync_token = state.get("sync_token")

    data = get_events(sync_token)

    events = data.get("items", [])
    next_sync_token = data.get("nextSyncToken")

    id_index, fallback_index = build_indexes()

    for e in events:
        event_id = e["id"]

        # törlés
        if e.get("status") == "cancelled":
            if event_id in id_index:
                archive_event(id_index[event_id])
            continue

        # external_id check
        if event_id in id_index:
            update_event(id_index[event_id], e)
            continue

        # fallback check
        event_key = build_event_key(e)

        if event_key in fallback_index:
            print("SKIP DUPLICATE:", event_key)
            continue

        # create
        create_event(e)

    if next_sync_token:
        state["sync_token"] = next_sync_token
        save_state(state)
