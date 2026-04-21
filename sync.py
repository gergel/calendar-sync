from google_api import get_events
from notion_api import create_event
from state import load_state, save_state


def run_sync():
    state = load_state()

    sync_token = state.get("sync_token")
    imported_ids = set(state.get("imported_ids", []))
    run_count = state.get("run_count", 0)

    print("RUN COUNT:", run_count)
    print("SYNC TOKEN:", sync_token)
    print("KNOWN IDS:", len(imported_ids))

    # 🔥 FIRST RUN → FULL IMPORT
    if run_count == 0:
        print("FIRST RUN → importing ALL events")

        data = get_events(None)
        events = data.get("items", [])
        next_sync_token = data.get("nextSyncToken")

        for e in events:
            if e.get("status") == "cancelled":
                continue

            create_event(e)
            imported_ids.add(e["id"])

        if next_sync_token:
            state["sync_token"] = next_sync_token

        state["imported_ids"] = list(imported_ids)
        state["run_count"] = 1

        save_state(state)

        print("FIRST RUN DONE")
        return

    # 🔥 NORMAL RUN
    data = get_events(sync_token)
    events = data.get("items", [])
    next_sync_token = data.get("nextSyncToken")

    print(f"Processing {len(events)} changes")

    for e in events:
        event_id = e["id"]

        if e.get("status") == "cancelled":
            continue

        if event_id in imported_ids:
            continue

        print("NEW EVENT:", e.get("summary"))

        create_event(e)
        imported_ids.add(event_id)

    if next_sync_token:
        state["sync_token"] = next_sync_token

    state["imported_ids"] = list(imported_ids)
    state["run_count"] = run_count + 1

    save_state(state)
