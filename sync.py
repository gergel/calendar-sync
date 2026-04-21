from google_api import get_events
from notion_api import create_event
from state import load_state, save_state


def run_sync():
    state = load_state()

    sync_token = state.get("sync_token")
    imported_ids = set(state.get("imported_ids", []))

    print("SYNC TOKEN:", sync_token)
    print("KNOWN IDS:", len(imported_ids))

    data = get_events(sync_token)

    events = data.get("items", [])
    next_sync_token = data.get("nextSyncToken")

    new_ids = set(imported_ids)

    print(f"Processing {len(events)} events")

    for e in events:
        event_id = e["id"]

        if e.get("status") == "cancelled":
            continue

        # 🔥 EZ A LÉNYEG
        if event_id in imported_ids:
            continue

        # új event
        create_event(e)
        new_ids.add(event_id)

    # sync token mentése
    if next_sync_token:
        state["sync_token"] = next_sync_token

    state["imported_ids"] = list(new_ids)

    save_state(state)
