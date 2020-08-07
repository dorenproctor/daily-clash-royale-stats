import requests
from bs4 import BeautifulSoup
import json
from time import time

def getText(elem):
    while elem.string == None: elem = next(elem.children)
    return elem.string.strip()

def parseSiteForStats(card_name, all_cards, errs):
    try:
        start_time = time()
        page = requests.get('https://clashroyale.fandom.com/wiki/'+card_name)
        soup = BeautifulSoup(page.text, 'html.parser')
        tables = soup.findAll("div", {"class": "table-back"})[0].findChildren(['table'])
        stats = {}
        for table in tables:
            data = {}
            categories = []
            headers = table.findChildren(['th'])
            cells = table.findChildren(['td'])
            for header in headers:
                categories.append(getText(header))
            if len(headers) == len(cells):
                for cell in cells:
                    data[categories.pop(0)] = getText(cell)
            else:
                i = 0
                sz = len(categories)
                for cell in cells:
                    vals = data.get(categories[i%sz])
                    if vals == None: vals = []
                    vals.append(getText(cell))
                    data[categories[i%sz]] = vals
                    i += 1
            stats[table.get('id')] = data
        all_cards[card_name] = stats
        print(card_name,'finished. Took',time()-start_time)
    except Exception as e:
        print(card_name,e)
        errs.append('{}: {}'.format(card_name,e))


with open('cards_to_query.json', 'r') as f:
    card_names = json.load(f)

all_cards = {}
errs = []
for card_name in card_names:
    parseSiteForStats(card_name, all_cards, errs)

with open('card_stats.json', 'w') as f:
    json.dump(all_cards, f)
    print('updated card_stats.json')