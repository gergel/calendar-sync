from notion_client import Client
import os

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DB_ID = os.getenv("NOTION_DB_ID")


def get_existing_ids():
    res = notion.databases.query(database_id=DB_ID)

    ids = set()

    for page in res["results"]:
        props = page["properties"]
        if "external_id" in props:
            val = props["external_id"]["rich_text"]
            if val:
                ids.add(val[0]["plain_text"])

    return ids


def upsert_event(event, existing_ids):
    event_id = event["id"]

    if event_id in existing_ids:
        # TODO: update
        return

    notion.pages.create(
        parent={"database_id": DB_ID},
        properties={
            "Name": {
                "title": [{"text": {"content": event.get("summary", "No title")}}]
            },
            "external_id": {
                "rich_text": [{"text": {"content": event_id}}]
            },
        },
    )


def delete_event(event_id):
    # TODO: keresd meg és archive-old
    pass
