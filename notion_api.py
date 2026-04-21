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


def build_indexes():
    pages = get_all_pages()

    id_index = {}
    fallback_index = set()

    for page in pages:
        props = page["properties"]

        # external_id
        ext = props.get("external_id", {}).get("rich_text", [])
        if ext:
            external_id = ext[0]["plain_text"]
            id_index[external_id] = page["id"]

        # fallback (name + date)
        name = props["Name"]["title"]
        date = props.get("Date", {}).get("date")

        if name and date:
            title = name[0]["plain_text"]
            start = date.get("start")
            end = date.get("end")

            key = f"{title}|{start}|{end}"
            fallback_index.add(key)

    return id_index, fallback_index


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


def build_event_key(event):
    title = event.get("summary", "No title")
    start, end = extract_dates(event)
    return f"{title}|{start}|{end}"


def create_event(event):
    start, end = extract_dates(event)

    notion.pages.create(
        parent={"database_id": DB_ID},
        properties={
            "Name": {
                "title": [{"text": {"content": event.get("summary", "No title")}}]
            },
            "Date": {
                "date": {"start": start, "end": end}
            },
            "external_id": {
                "rich_text": [{"text": {"content": event["id"]}}]
            },
        },
    )


def update_event(page_id, event):
    start, end = extract_dates(event)

    notion.pages.update(
        page_id=page_id,
        properties={
            "Name": {
                "title": [{"text": {"content": event.get("summary", "No title")}}]
            },
            "Date": {
                "date": {"start": start, "end": end}
            },
        },
    )


def archive_event(page_id):
    notion.pages.update(page_id=page_id, archived=True)
