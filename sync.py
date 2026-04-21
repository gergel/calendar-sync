from google_api import get_events
from notion_api import create_event, update_event, archive_event
from state import load_state, save_state


def run_sync():
    state = load_state()
    sync_token = state.get("sync_token")

    # 🔥 FIRST RUN → csak baseline
    if not sync_token:
        print("FIRST RUN → only saving sync token")

        data = get_events(None)
        next_sync_token = data.get("nextSyncToken")

        if next_sync_token:
            state["sync_token"] = next_sync_token
            save_state(state)

        print("Baseline saved. No events created.")
        return

    # 🔥 NORMAL RUN
    data = get_events(sync_token)

    events = data.get("items", [])
    next_sync_token = data.get("nextSyncToken")

    print(f"Processing {len(events)} changes")

    for e in events:
        event_id = e["id"]

        # törlés
        if e.get("status") == "cancelled":
            archive_event(event_id)
            continue

        # update / create
        if e.get("status") == "confirmed":
            create_event(e)  # ⚠️ csak újakat kezelünk

    # mentjük a következő tokent
    if next_sync_token:
        state["sync_token"] = next_sync_token
        save_state(state)
