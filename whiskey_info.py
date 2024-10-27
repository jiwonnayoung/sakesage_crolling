from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
from selenium.common.exceptions import UnexpectedAlertPresentException



# MySQL 연결 설정
db_config = {
    'user': 'admin',
    'password': 'tkzptkzptkrp24',
    'host': 'database-sakesage.c3suqkcwcjd4.ap-northeast-2.rds.amazonaws.com',
    'database': 'sakesage'
}

# MySQL에 데이터 저장 함수
def save_data_to_mysql(name, aroma, taste, finish, kind, alcohol_content, country, explanation):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 데이터 삽입
        query = "INSERT INTO whiskey_info (name, aroma, taste, finish, kind, alcohol_content, country, explanation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, aroma, taste, finish, kind, alcohol_content, country, explanation))
        conn.commit()
        print(f"데이터가 MySQL에 저장되었습니다. ({name})")
    except mysql.connector.Error as error:
        print(f"MySQL 에러: {error}")
    finally:
        cursor.close()
        conn.close()


# URL 리스트
urls = [
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000112",#글렌 그란트 10년 グレングラント10年 (도쿄 -긴자)
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000448", #달모어 12년 ダルモア１２年 (도쿄 - 긴자) - dalmore 12 
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000001729", #글렌 고인 10년 700ML グレンゴイン10年 (도쿄 - 긴자) glengoyne 10 years
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000113", # 글렌 그란트 15년 배치 스트렝스 グレングラント 15年 700ml GB glen grant 15
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000160", # 네이키드 몰트  ネイキッドモルト 40%naked malt
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000130" , #발렌타인 17년 バランタイン17年 750ml(箱無)ballantine 17 years
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000447", # 조니워커 그린 15년 ジョニーウォーカー アイランドグリーン1L(箱付)Johnnie Walker Island Green 1L
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000002202" # 조니워커 블랙 ジョニーウォーカーブラックトリプルカスク johnnie walker black triple cask
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000002787", #조니워커 블론드  ジョニー ウォーカー ブロンド johnnie walker blonde
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000439", # 탐나불린 스패니시 레드와인 , 타므나브린
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000114", #글렌그란트 아보랄리스, 알보랄리스
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000422", #글렌알라키 2012 빈티지 뀌베 와인 캐스크 피니쉬
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000540", # 글렌알라키 7년 헝가리안 버진 오크, 글렌 알라히 헝가리안 어쩌고
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000001495", #시바스 리갈 12년 700ML
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000545",# 코인트로, 코안트로 마가리타
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000187",#오켄토션 아메리칸 오크 ,오헨토산 아메리칸 오크 700ML
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000000161",#달모어 15년, 
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000002492",# 토버모리 12년, 토바모리
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000001677",# 웨스트콕 아이리쉬 블렌디드 버번 캐스크, 웨스트 코크 아이리쉬 버번 캐스크
    "https://m.kihya.com/goods/goods_view.php?goodsNo=1000001678",# 웨스트콕 아이리쉬 쉐리 캐스크, 웨스트코크 아이리쉬 캐스크 스트롱스
]

# 웹 드라이버 설정
driver = webdriver.Chrome()

# 결과를 저장할 리스트
results = []

# 각 URL에 대해 크롤링
for url in urls:
    try: 
        driver.get(url)
        # 페이지 로드 대기 (필요에 따라 조정)
        driver.implicitly_wait(10)
        
        # 페이지 소스 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        name = soup.select_one("#product_name.mb-0.fw-bold.fs-4").text.strip().replace(' ','')
        
        # Aroma, Taste, Finish 텍스트 추출
        tasting_notes_ul = soup.find('h4', id='tasting-notes').find_next('ul')
        aroma = tasting_notes_ul.find_all('li')[0].get_text(strip=True).replace('Aroma', '').strip()
        taste = tasting_notes_ul.find_all('li')[1].get_text(strip=True).replace('Taste', '').strip()
        finish = tasting_notes_ul.find_all('li')[2].get_text(strip=True).replace('Finish', '').strip()
        
        # 종류, 도수, 국가 추출
        information_ul = soup.find('h4', id='information').find_next('ul')
        details_li = information_ul.find_all('li')
        
        kind = details_li[0].get_text(strip=True).replace('종류', '').strip() if len(details_li) > 0 else 'N/A'
        alcohol_content = details_li[2].get_text(strip=True).replace('도수', '').strip() if len(details_li) > 2 else 'N/A'
        country = details_li[3].get_text(strip=True).replace('국가', '').strip() if len(details_li) > 3 else 'N/A'

        # 첫 번째 p 태그의 텍스트 추출
        explain_text = soup.select_one('.product-detail > p')
        if explain_text:
            explain_text = explain_text.get_text(strip=True)
        else:
            explain_text = 'N/A'

        

        
        
        result = {
            "name": name,
            "aroma": aroma,
            "taste": taste,
            "finish": finish,
            "kind": kind,
            "alcohol_content": alcohol_content,
            "country": country,
            "explanation" : explain_text
        }

        # MySQL에 데이터 저장
        save_data_to_mysql(name, aroma, taste, finish, kind, alcohol_content, country, explain_text)

        
        results.append(result)
    except Exception as e:
        print(f"Error occurred while processing URL {url}: {e}")

        
# 브라우저 닫기
driver.quit()

# # 결과 출력
# for result in results:
#     print(f"이름: {result['name']}\nAroma: {result['aroma']}\nTaste: {result['taste']}\nFinish: {result['finish']}\n종류: {result['kind']}\n도수: {result['alcohol_content']}\n국가: {result['country']}\n설명: {result['explanation']}\n")