import requests
from bs4 import BeautifulSoup
import json
from time import time

card_names = ['Archers', 'Arrows', 'Baby_Dragon', 'Balloon', 'Bandit', 'Barbarian_Barrel', 'Barbarian_Hut', 'Barbarians', 'Bats', 'Battle_Healer', 'Battle_Ram', 'Bomb_Tower', 'Bomber', 'Bowler', 'Cannon', 'Cannon_Cart', 'Clone', 'Dark_Prince', 'Dart_Goblin', 'Earthquake', 'Electro_Dragon', 'Electro_Wizard', 'Elite_Barbarians', 'Elixir_Collector', 'Elixir_Golem', 'Executioner', 'Fire_Spirits', 'Fireball', 'Firecracker', 'Fisherman', 'Flying_Machine', 'Freeze', 'Furnace', 'Giant', 'Giant_Skeleton', 'Giant_Snowball', 'Goblin_Barrel', 'Goblin_Cage', 'Goblin_Gang', 'Goblin_Giant', 'Goblin_Hut', 'Goblins', 'Golem', 'Graveyard', 'Guards', 'Heal', 'Hog_Rider', 'Hunter', 'Ice_Golem', 'Ice_Spirit', 'Ice_Wizard', 'Inferno_Dragon', 'Inferno_Tower', 'Knight', 'Lava_Hound', 'Lightning', 'Lumberjack', 'Magic_Archer', 'Mega_Knight', 'Mega_Minion', 'Miner', 'Mini_P.E.K.K.A.', 'Minion_Horde', 'Minions', 'Mirror', 'Mortar', 'Musketeer', 'Night_Witch', 'P.E.K.K.A.', 'Poison', 'Prince', 'Princess', 'Rage', 'Ram_Rider', 'Rascals', 'Rocket', 'Royal_Ghost', 'Royal_Giant', 'Royal_Hogs', 'Royal_Recruits', 'Skeleton_Army', 'Skeleton_Barrel', 'Skeletons', 'Sparky', 'Spear_Goblins', 'Tesla', 'The_Log', 'Three_Musketeers', 'Tombstone', 'Tornado', 'Valkyrie', 'Wall_Breakers', 'Witch', 'Wizard', 'X-Bow', 'Zap', 'Zappies']

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

all_cards = {}
errs = []
for card_name in card_names:
    parseSiteForStats(card_name, all_cards, errs)

with open('card_stats.json', 'w') as f:
    json.dump(all_cards, f)