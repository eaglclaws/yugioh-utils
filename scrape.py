import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url_head = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=2&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page="

browser = webdriver.Firefox()
browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action")
browser.find_element(By.ID, 'submit_area').click()
time.sleep(2)
browser.find_element(By.ID, 'mode_set').find_elements(By.TAG_NAME, 'li')[1].click()
browser.get("https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&rp=100&mode=2&stype=1&link_m=2&othercon=2&sort=1&request_locale=ko&page=1")

for i in range(2, 119):
    browser.get(url_head + str(i))
    time.sleep(0.5)

soup = BeautifulSoup(browser.page_source, 'lxml')

print(soup.find("div", {"id": "card_list"}).prettify())
browser.quit()
