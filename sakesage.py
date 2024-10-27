import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from urllib.parse import urljoin
from googletrans import Translator

# MySQL 연결 설정
db_config = {
    'user': 'admin',
    'password': 'tkzptkzptkrp24',
    'host': 'database-sakesage.c3suqkcwcjd4.ap-northeast-2.rds.amazonaws.com',
    'database': 'sakesage'
}

# MySQL에 데이터 저장 함수
def save_data_to_mysql(translated_title, price, translated_taste, image_url, site_name, name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 데이터 삽입
        query = "INSERT INTO sake_info (title, price, taste, image_url, site_name, name) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (translated_title, price, translated_taste, image_url, site_name, name))
        conn.commit()
        print("데이터가 MySQL에 저장되었습니다.")
    except mysql.connector.Error as error:
        print(f"MySQL 에러: {error}")
    finally:
        cursor.close()
        conn.close()

# 이미지 다운로드 함수
def get_image_url(img_url):
    try:
        if img_url.startswith('/'):  # 상대 경로인 경우
            img_url = urljoin(base_url, img_url)  # 절대 경로로 변환
        return img_url
    except Exception as e:
        print(f"이미지 URL 가져오기 실패: {e}")
        return None

# 번역 함수
def translate_text(text, dest_lang='ko'):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest_lang)
    return translated_text.text

# 카테고리
categories = {
    '21': '청주',
    '26': '양주'
}

site_names = [
    #---도쿄---#
    #"야마야 도쿄 긴자점",
    #"야마야 도쿄 신주쿠점",
    #"야마야 도쿄 이케부쿠로 서점",
    #"야마야 도쿄 이케부쿠로 히가시점",
    #"야마야 도쿄 기타노다이점",
    #"야마야 도쿄 고지마치 한조몬점",
    #"야마야 도쿄 오모리점",
    #"야마야 도쿄 히가시야마토점",
    #"야마야 도쿄 무사시무라야마잔호리점",
    #"야마야 도쿄 카메이도점",
    #---오사카---#
    #"야마야 오사카 나가호리바시점",
    #"야마야 오사카 가와치 반선점",
    #"야마야 오사카 사이지점",
    #"야마야 오사카 미나미부키다점",
    #"야마야 오사카 스이타 센리오카점",
    #"야마야 오사카 이즈미추오점",
    #"야마야 오사카 도지마 플라자점",
    #"야마야 오사카 성동 히가시나카하마점",
    #"야마야 오사카  오기리점",
    #"야마야 오사카 히가시요도가와 스가와라점",
    #---후쿠오카---#
    "야마야 후쿠오카 고가점",
    "야마야 후쿠오카 치고점",
    "야마야 후쿠오카 다이묘점",
    "야마야 후쿠오카 나가하마점",
    "야마야 후쿠오카 오구스점",
    "야마야 후쿠오카 이마주쿠점",
    "야마야 후쿠오카 조카하마 오도점",
    "야마야 후쿠오카 시면점",
    "야마야 후쿠오카 나카가와점",

]

# 이미지를 저장할 폴더 생성
image_folder = "images"
os.makedirs(image_folder, exist_ok=True)

# 기본 URL
base_url = "https://drive.yamaya.jp/"

# Translator 객체 생성
translator = Translator()

for site_name, site_url in zip(site_names, [
   #"https://drive.yamaya.jp/40417/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40402/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40403/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40401/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40420/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40409/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40416/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40423/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40426/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40412/catalog/list.php?CLASS={}&page={}",

   #"https://drive.yamaya.jp/40809/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40765/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40864/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40865/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40866/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40898/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40816/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40872/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40877/catalog/list.php?CLASS={}&page={}",
   #"https://drive.yamaya.jp/40876/catalog/list.php?CLASS={}&page={}",

   "https://drive.yamaya.jp/40944/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40931/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40945/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40926/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40934/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40929/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40949/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40927/catalog/list.php?CLASS={}&page={}",
   "https://drive.yamaya.jp/40937/catalog/list.php?CLASS={}&page={}",

   # Add more URLs if needed
]):
    for category, name in categories.items():
        for pageNum in range(1, 2):
            response = requests.get(site_url.format(category, pageNum))
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            words = soup.select('.card')

            for idx, word in enumerate(words, start=1):
                translated_taste=""

                title = word.select_one('a.d-block').text.strip()
                taste_element = word.select_one('.card-body p.card-text:not(.text-right)')
                taste = taste_element.text.strip() if taste_element else ""

                price_elements = word.select_one('p.card-text.text-right span')
                price_text = ''.join([element.get_text(strip=True) for element in price_elements])
                price = price_text.strip()

                translated_title = ""
                chunk_size = 5000
                for i in range(0, len(title), chunk_size):
                    chunk = title[i:i + chunk_size]
                    translated_chunk = translate_text(chunk, dest_lang='ko')
                    translated_title += translated_chunk

                if taste:
                    for i in range(0, len(taste), chunk_size):
                        chunk = taste[i:i + chunk_size]
                        translated_chunk = translate_text(chunk, dest_lang='ko')
                        translated_taste += translated_chunk

                img_url = word.select_one('img.card-img.mx-auto.d-block')['src']
                image_url = get_image_url(img_url)
                if image_url:
                    save_data_to_mysql(translated_title, price, translated_taste, image_url, site_name, name)
