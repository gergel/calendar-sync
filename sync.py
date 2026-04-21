from google_api import get_events
from notion_api import create_event, update_event, archive_event, build_index
from state import load_state, save_state


def run_sync():
    state = load_state()
    sync_token = state.get("sync_token")

    data = get_events(sync_token)

    events = data.get("items", [])
    next_sync_token = data.get("nextSyncToken")

    notion_index = build_index()

    for e in events:
        event_id = e["id"]

        # törlés
        if e.get("status") == "cancelled":
            if event_id in notion_index:
                archive_event(notion_index[event_id])
            continue

        # update
        if event_id in notion_index:
            update_event(notion_index[event_id], e)
        else:
            create_event(e)

    if next_sync_token:
        state["sync_token"] = next_sync_token
        save_state(state)
