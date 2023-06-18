import json

def card_with_name(name, data):
    for key in data:
        if data[key]["name"] == name:
            return data[key]

with open('database.json', 'r', encoding='utf-8') as file:
    database = json.load(file)

with open('cardlist.sw', 'r', encoding='utf-8') as file:
    card_list = file.read().splitlines()

cards = []
second_level = dict()
third_level = dict()

for card in card_list:
    cards.append(card_with_name(card, database))

for card1 in cards:
    for card2 in cards:
        if card1 is card2:
            continue
        else:
            match = 0
            if (card1["type"][0] == card2["type"][0]):
                match = match + 1
            if (card1["attribute"] == card2["attribute"]):
                match = match + 1
            if (card1["level"] == card2["level"]):
                match = match + 1
            if (card1["atk"] == card2["atk"]):
                match = match + 1
            if (card1["def"] == card2["def"]):
                match = match + 1
            if match != 1:
                continue
            else:
                if not card1["name"] in second_level:
                    second_level[card1["name"]] = []
                second_level[card1["name"]].append(card2["name"])

for one in card_list:
    for two in second_level[one]:
        for three in second_level[two]:
            if one == three:
                continue
            else:
                print(one + " -> " + two + " -> " + three)
