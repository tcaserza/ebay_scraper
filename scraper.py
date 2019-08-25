#!/usr/bin/env python
from ebaysdk.finding import Connection
from datetime import datetime, timedelta
import requests
import json

DEBUG = False


def date_add_hours(hours_to_add):
    return (datetime.now() + timedelta(hours=hours_to_add)).strftime("%Y-%m-%dT%H:%M:%S")


def find_it(search, existing_ids):
    api = Connection(config_file='ebay.yaml', debug=DEBUG, siteid="EBAY-US")
    response = api.execute('findItemsByKeywords', search)
    result_list = []
    if response.reply.paginationOutput.totalEntries != "0":
        for item in response.reply.searchResult.item:
            if str(item.itemId) not in existing_ids:
                result_list.append({"item_id": item.itemId,
                                    "title": item.title,
                                    "end_date": item.listingInfo.endTime,
                                    "price": item.sellingStatus.currentPrice.value
                                    })
    return result_list


def get_existing_item_ids():
    url = 'http://pibay/ebay/listitemids'
    response = requests.get(url)
    return json.loads(response.content)['response']


def input_items(items):
    data = []
    url = 'http://pibay/ebay/add'
    for item in items:
        data.append({
            "item_id": item['item_id'],
            "title": item['title'],
            "end_date": item['end_date'].strftime("%Y%m%dT%H:%M:%S"),
            "price": item['price']
            })
    response = requests.post(url, json=data)
    print response
    

def load_searches():
    searches = []
    with open("searches.txt") as f1:
        for line in f1.readlines():
            searches.append({line.split('|')[0]: line.split('|')[1].rstrip('\n')})
    print searches
    return searches


if __name__ == '__main__':
    existing_ids = get_existing_item_ids()
    searches = load_searches()
    for search in searches:
        found_items = find_it(search, existing_ids)
        input_items(found_items)


