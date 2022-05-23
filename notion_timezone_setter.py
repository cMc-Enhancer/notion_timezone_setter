from json import JSONDecodeError

import requests
import properties
import os

base_url = "https://api.notion.com/v1/"

env = os.environ
if env.get("NOTION_TOKEN"):
    NOTION_TOKEN = env.get("NOTION_TOKEN")
    DATABASE_ID = env.get("NOTION_DATABASE_ID")
    DATE_COLUMN_NAME = env.get("NOTION_DATE_COLUMN_NAME")
else:
    NOTION_TOKEN = properties.NOTION_TOKEN
    DATABASE_ID = properties.DATABASE_ID
    DATE_COLUMN_NAME = properties.DATE_COLUMN_NAME

header = {"Authorization": NOTION_TOKEN, "Notion-Version": "2022-02-22", "Content-Type": "application/json"}


def query(start_cursor):
    if start_cursor == "":
        body = '{}'
    else:
        body = '{"start_cursor": "' + str(start_cursor) + '"}'
    return requests.post(base_url + "databases/" + DATABASE_ID + "/query", headers=header, data=body).json()


def update_page_date(page):
    page_id = page["id"]
    start = page["properties"][DATE_COLUMN_NAME]["date"]["start"]
    current_time_zone = page["properties"][DATE_COLUMN_NAME]["date"]["time_zone"]

    if current_time_zone == "Asia/Shanghai":
        return

    start = str(start).split('.')[0]
    body = '{"properties": {"' + DATE_COLUMN_NAME + '": {"date": {"start": "' + start + '","time_zone":"Asia/Shanghai"}}}}'
    return __retry_patch(base_url + "pages/" + page_id, header, body.encode('utf-8'))


def __retry_patch(url, header, body):
    try:
        resp = requests.patch(url, headers=header, data=body).json()
    except JSONDecodeError:
        resp = __retry_patch(url, header, body)

    return resp


pages = []
has_more = True
start_cursor = ""
while has_more:
    response = query(start_cursor)
    has_more = response["has_more"]
    start_cursor = response["next_cursor"]
    pages.extend(response["results"])
for p in pages:
    response = update_page_date(p)
    print(update_page_date(p))
