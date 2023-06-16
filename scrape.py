import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url_head = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=2&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page="

browser = webdriver.Firefox()
browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action")
browser.find_element(By.ID, 'submit_area').click()
browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=1&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page=1")

database = dict()

for page in range(1, 120):
    card_num = 0
    browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=1&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page=" + str(page))
    soup = BeautifulSoup(browser.page_source, 'lxml')
    card_list = soup.find("div", {"id": "card_list"}).extract()
    card_rows = card_list.find_all("div", {"class": "t_row"})
    for card in card_rows:
        cid = re.search(r'\d+$', card.find("input", {"class": "link_value"})["value"]).group()
        card_name = card.find("dd", {"class": "box_card_name"}).find("span", {"class": "card_name"}).text.strip()
        card_text = card.find("dd", {"class": "box_card_text"}).text.strip()
        card_spec = list(map(lambda span: span.text.replace("\u0009", "").replace("\u000A", "").replace("\u00A0", " ").strip(), card.find("dd", {"class": "box_card_spec"}).find_all("span", recursive=False)))
        print(card_name)
        database[cid] = dict()
        database[cid]["name"] = card_name
        database[cid]["text"] = card_text
        if len(card_spec) > 2:
            database[cid]["card_type"] = "몬스터"
            database[cid]["attribute"] = card_spec[0]
            database[cid]["level"] = re.search(r'\d+$', card_spec[1]).group()
            type_list = card_spec[2].replace('[', '').replace(']', '').split('/')
            database[cid]["type"] = type_list
            database[cid]["atk"] = re.search(r'\d+$|\?$', card_spec[3]).group()
            database[cid]["def"] = re.search(r'\d+$|\?$|\-$', card_spec[4]).group()
        else:
            database[cid]["card_type"] = card_spec[0]
            database[cid]["type"] = card_spec
        card_num = card_num + 1

with open('database.json', 'w', encoding='utf-8') as file:
    json.dump(database, file, ensure_ascii=False, indent=4)

browser.quit()
