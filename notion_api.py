from notion_client import Client
import os

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DB_ID = os.getenv("NOTION_DB_ID")


def extract_dates(event):
    start = None
    end = None

    if event.get("start", {}).get("dateTime"):
        start = event["start"]["dateTime"]
    elif event.get("start", {}).get("date"):
        start = event["start"]["date"] + "T00:00:00"

    if event.get("end", {}).get("dateTime"):
        end = event["end"]["dateTime"]
    elif event.get("end", {}).get("date"):
        end = event["end"]["date"] + "T00:00:00"

    return start, end


def create_event(event):
    start, end = extract_dates(event)

    notion.pages.create(
        parent={"database_id": DB_ID},
        properties={
            "Name": {
                "title": [
                    {"text": {"content": event.get("summary", "No title")}}
                ]
            },
            "Date": {
                "date": {
                    "start": start,
                    "end": end
                }
            },
            "external_id": {
                "rich_text": [
                    {"text": {"content": event["id"]}}
                ]
            },
        },
    )


def archive_event(event_id):
    # egyszerű fallback: nem keresünk vissza
    print(f"Event deleted in Google (ignored in Notion): {event_id}")


def update_event(page_id, event):
    pass  # nem használjuk
