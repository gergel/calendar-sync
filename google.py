import requests
import os

API_KEY = os.getenv("GOOGLE_API_KEY")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")


def get_events(sync_token=None):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"

    params = {
        "maxResults": 250,
        "singleEvents": False,
        "showDeleted": True,
    }

    if sync_token:
        params["syncToken"] = sync_token
    else:
        params["timeMin"] = "2026-03-01T00:00:00Z"

    res = requests.get(url, params=params)
    res.raise_for_status()

    return res.json()
