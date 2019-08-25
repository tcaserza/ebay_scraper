#!/usr/bin/env python
from ebaysdk.finding import Connection
from datetime import datetime, timedelta


DEBUG=False

def date_add_hours(hours_to_add):
    return (datetime.now() + timedelta(hours=hours_to_add)).strftime("%Y-%m-%dT%H:%M:%S")


def find_it(search):
    api = Connection(config_file='ebay.yaml', debug=DEBUG, siteid="EBAY-US")
    response = api.execute('findItemsByKeywords', search)
    if response.reply.paginationOutput.totalEntries != "0":
        for item in response.reply.searchResult.item:
            print("Title: %s, Price: %s" % (item.title, item.sellingStatus.currentPrice.value))


searches = [
    {
        'keywords': 'ken griffey jr 1989 upper deck card psa -(topps reprint donruss trump bowman packs)',
        'itemFilter': [
            {'name': 'MaxPrice', 'value': '20.00'},
            {'name': 'EndTimeTo', 'value': date_add_hours(32)}
            ],
        'sortOrder': 'PricePlusShippingLowest'
    },
    {
        'keywords': 'ken griffey jr 1989 upper deck card psa -(topps reprint donruss trump bowman packs)',
        'itemFilter': [
            {'name': 'MaxPrice', 'value': '20.00'},
            {'name': 'ListingType', 'value': 'FixedPrice'}
            ],
        'sortOrder': 'PricePlusShippingLowest'
    }
]

if __name__ == '__main__':
    for search in searches:
        find_it(search)
