import requests
import os


def refresh_token():
    res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
            "grant_type": "refresh_token",
        },
    )

    if not res.ok:
        print("TOKEN ERROR:", res.text)
        res.raise_for_status()

    return res.json()["access_token"]


def get_events(sync_token=None):
    access_token = refresh_token()

    url = f"https://www.googleapis.com/calendar/v3/calendars/{os.getenv('GOOGLE_CALENDAR_ID')}/events"

    params = {
        "maxResults": 250,
        "showDeleted": True,
        "singleEvents": False,
    }

    if sync_token:
        params["syncToken"] = sync_token
    else:
        params["timeMin"] = "2026-03-01T00:00:00Z"
        params["orderBy"] = "updated"

    res = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
    )

    data = res.json()

    print("GOOGLE RESPONSE COUNT:", len(data.get("items", [])))

    if not res.ok:
        print("GOOGLE ERROR:", res.text)
        res.raise_for_status()

    return data
