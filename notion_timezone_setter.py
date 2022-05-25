from json import JSONDecodeError

import requests
import properties
import os
import concurrent.futures

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

    if str(start).endswith("+08:00"):
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


def main():
    pages = []
    has_more = True
    start_cursor = ""
    while has_more:
        response = query(start_cursor)
        has_more = response["has_more"]
        start_cursor = response["next_cursor"]
        pages.extend(response["results"])

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_page = {executor.submit(update_page_date, p): p for p in pages}
        for future in concurrent.futures.as_completed(future_to_page):
            response = future.result()
            if response is not None:
                print(response)


if __name__ == '__main__':
    main()
