import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import mysql.connector

# MySQL 연결 설정
db_config = {
    'user': 'admin',
    'password': 'tkzptkzptkrp24',
    'host': 'database-sakesage.c3suqkcwcjd4.ap-northeast-2.rds.amazonaws.com',
    'database': 'sakesage'
}

# MySQL에 데이터 저장 함수
def save_store_info_to_mysql(store_name, address, phone, business_hours, city_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 데이터 삽입
        query = "INSERT INTO sake_store_info (store_name, address, phone, business_hours, city_name) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (store_name, address, phone, business_hours, city_name))
        conn.commit()
        print("데이터가 MySQL에 저장되었습니다.")
    except mysql.connector.Error as error:
        print(f"MySQL 에러: {error}")
    finally:
        cursor.close()
        conn.close()

def get_city_name(city_code):
    if city_code == 13:
        return "도쿄"
    elif city_code == 27:
        return "오사카"
    elif city_code == 40:
        return "후쿠오카"
    else:
        return "Unknown"

def get_store_info(cdpref):
    url = f"https://www.yamaya.jp/ynhp/contents/stores/store_list.php?CDPREF={cdpref}"
    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select(".shop.mb-2")

    translator = Translator()

    for item in items:
        store = item.select_one("h4.block-heading.list")
        address = item.select_one("tr.address .shop-information-text")
        phone_element = item.select_one("tr.telephone .shop-information-text a")
        time = item.select_one("tr.business-hours .shop-information-text")

        store_text = store.get_text(strip=True) if store else "No store name found"
        address_text = address.get_text(strip=True) if address else "No address found"
        phone_text = phone_element['href'].replace('tel:', '') if phone_element else "No phone found"
        time_text = time.get_text(strip=True) if time else "No business hours found"

        # Translate to Korean
        store_text_kr = translator.translate(store_text, src='ja', dest='ko').text
        address_text_kr = translator.translate(address_text, src='ja', dest='ko').text
        phone_text_kr = translator.translate(phone_text, src='ja', dest='ko').text
        time_text_kr = translator.translate(time_text, src='ja', dest='ko').text if time_text else "No business hours found"

        # Convert city code to text
        city_name = get_city_name(cdpref)

        # Save to MySQL
        save_store_info_to_mysql(store_text_kr, address_text_kr, phone_text_kr, time_text_kr, city_name)

# 13=도쿄, 27=오사카, 40=후쿠오카
cdprefs = [13, 27, 40]
for cdpref in cdprefs:
    get_store_info(cdpref)
