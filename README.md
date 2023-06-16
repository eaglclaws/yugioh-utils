# Yu-Gi-Oh<sup>TM</sup> utils
A series of small scripts to help Yu-Gi-Oh<sup>TM</sup> players

## PotOfGreed
A webscraper for the [official Yu-Gi-Oh<sup>TM</sup> database](db.yugioh-card.com)

[공식 유희왕<sup>TM</sup> 데이터베이스](db.yugioh-card.com)용 웹 스크래퍼
### Usage
PotOfGreed uses selenium, be sure to install a compatible webdriver first. (This script uses geckodriver.)

Selenium을 활용하고 있기 때문에 웹 드라이버 설치가 필요합니다. (본 스크립트는 geckodriver를 이용합니다.)
```
pip install -r requirements.txt
python3 potofgreed.py
```
After completion, POG should have created a file called "database.json"

실행 종료 후, "database.json" 파일을 생성합니다.

## SmallWorld
A route finder for the card "Small World"

"스몰 월드" 루트 생성기
### Usage
Create a file called "cardlist.sw" and enter the cards you wish to iterate through on its own line.

"cardlist.sw"에 탐색할 카드를 한 줄씩 입력합니다.
```
python3 smallword.py
```
