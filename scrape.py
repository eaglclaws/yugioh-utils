import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm

url_head = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=2&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page="
database = dict()

browser = webdriver.Firefox()

#Witchcraft to get direct link page traversal to work; without this, no matter what the site takes you to the landing page
#직접 링크로 페이지 이동을 할 수 있게 해주는 흑마법. 이 동작 없이는 사이트가 항상 초기 페이지로 이동한다.
browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action")
browser.find_element(By.ID, 'submit_area').click()
browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=1&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page=1")

for page in tqdm(range(1, 120)):
    card_num = 0
    #Noteable query options:
    #   rp: the number of rows per page; can be set to 10, 50, or 100
    #   mode: the view of the database; 1 for images, 2 for text only (text only mode omits card text)
    #   request_locale: the language of the database.
    #       Japanese: ja
    #       English: en
    #       French: fr
    #       German: de
    #       Italian: it
    #       Spanish: es
    #       Portuguese: pt
    #       Korean: ko
    #   page: current viewing page of the database
    #기억하면 좋은 쿼리 매개변수:
    #   rp: 페이지 당 표시 되는 행의 갯수. 10, 50, 100 중에 하나로 설정할 수 있다.
    #   mode: 데이터베이스 표시 방식. 1은 이미지 표시, 2는 텍스트 표시 (단, 텍스트 표시 시에는 카드 텍스트는 생략 된다.)
    #   request_locale: 데이터베이스 언어 설정.
    #       일본어: ja
    #       영어: en
    #       프랑스어: fr
    #       독일어: de
    #       이탈리아어: it
    #       스페인어: es
    #       포르투갈어: pt
    #       한국어: ko
    #   page: 현재 보고 있는 데이터베이스 페이지
    browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=1&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page=" + str(page))
    soup = BeautifulSoup(browser.page_source, 'lxml')
    card_list = soup.find("div", {"id": "card_list"}).extract()
    card_rows = card_list.find_all("div", {"class": "t_row"})
    for card in card_rows:
        #Futureproofing for potential updates to the database. When rescraping the database, [cid in database] can be used to check for duplicates.
        #추후에 업데이트할 경우가 생기면 편하게 중복 추리기 위한 대비. [cid in database]의 여부를 확인하고 중복 검증을 편하게 할 수 있다.
        cid = re.search(r'\d+$', card.find("input", {"class": "link_value"})["value"]).group()

        #Change codepoint U+FF0D to '-' so names can be typed on the keyboard. Although not aesthetically pleasing, makes writing scripts much easier.
        #U+FF0D를 '-'로 바꿔서 카드명을 편하게 입력할 수 있도록했다. (예시: 섬도희－레이 -> 섬도희-레이) 심지적으로 별로지만, 스크립트 작성시에 편하다.
        card_name = card.find("dd", {"class": "box_card_name"}).find("span", {"class": "card_name"}).text.strip().replace('－', '-')
        card_text = card.find("dd", {"class": "box_card_text"}).text.strip().replace('－', '-')
        
        #There are A LOT of unwanted characters in the original text. Lazy way of removing all of that.
        #불필요한 문자가 굉장히 많았다. 빠르고 지저분하게 지웠다.
        card_spec = list(map(lambda span: span.text.replace("\u0009", "").replace("\u000A", "").replace("\u00A0", " ").strip(), card.find("dd", {"class": "box_card_spec"}).find_all("span", recursive=False)))
        
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
