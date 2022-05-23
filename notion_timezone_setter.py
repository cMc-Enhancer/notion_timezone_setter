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


def query():
    return requests.post(base_url + "databases/" + DATABASE_ID + "/query", headers=header, data='{}')


def update_page_date(page):
    page_id = page["id"]
    start = page["properties"][DATE_COLUMN_NAME]["date"]["start"]
    start = str(start).split('.')[0]
    body = '{"properties": {"' + DATE_COLUMN_NAME + '": {"date": {"start": "' + start + '","time_zone":"Asia/Shanghai"}}}}'
    return requests.patch(base_url + "pages/" + page_id, headers=header, data=body.encode('utf-8'))


pages = query().json()["results"]
for p in pages:
    print(update_page_date(p).json())
