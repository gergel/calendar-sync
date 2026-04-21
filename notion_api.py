from notion_client import Client
import os

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DB_ID = os.getenv("NOTION_DB_ID")


def get_all_pages():
    pages = []
    cursor = None

    while True:
        res = notion.databases.query(
            database_id=DB_ID,
            start_cursor=cursor
        )
        pages.extend(res["results"])

        if not res.get("has_more"):
            break
        cursor = res["next_cursor"]

    return pages


def build_index():
    pages = get_all_pages()
    index = {}

    for page in pages:
        props = page["properties"]
        ext = props["external_id"]["rich_text"]

        if ext:
            external_id = ext[0]["plain_text"]
            index[external_id] = page["id"]

    return index


def create_event(event):
    notion.pages.create(
        parent={"database_id": DB_ID},
        properties={
            "Name": {
                "title": [{"text": {"content": event.get("summary", "No title")}}]
            },
            "external_id": {
                "rich_text": [{"text": {"content": event["id"]}}]
            },
        },
    )


def update_event(page_id, event):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Name": {
                "title": [{"text": {"content": event.get("summary", "No title")}}]
            }
        },
    )


def archive_event(page_id):
    notion.pages.update(page_id=page_id, archived=True)
