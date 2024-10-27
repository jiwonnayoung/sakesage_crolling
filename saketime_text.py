from selenium import webdriver
from bs4 import BeautifulSoup
from googletrans import Translator
import mysql.connector

# 구글 번역 객체 생성
translator = Translator()

#MySQL 연결 설정
db_config = {
    'user': 'admin',
    'password': 'tkzptkzptkrp24',
    'host': 'database-sakesage.c3suqkcwcjd4.ap-northeast-2.rds.amazonaws.com',
    'database': 'sakesage'
}

def save_data_to_mysql(title, explain, reviews, dates, writers, scores):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 데이터 삽입
        query = "INSERT INTO sake_review (sake_title, explanation, review, date, writer, score) VALUES (%s, %s, %s, %s, %s, %s)"
        for review, date, writer, score in zip(reviews, dates, writers, scores):
            cursor.execute(query, (title, explain, review, date, writer, score))
        conn.commit()
        print("데이터가 MySQL에 저장되었습니다.")
    except mysql.connector.Error as error:
        print(f"MySQL 에러: {error}")
    finally:
        cursor.close()
        conn.close()

# 웹 드라이버 설정
driver = webdriver.Chrome()  # 크롬 드라이버 경로 설정 필요

# 여러 URL에 대해 순차적으로 크롤링
urls = [
    #"https://www.saketime.jp/brands/696", #도쿄- 이케부쿠로 서점越後鶴亀 純米大吟醸(에치고 츠루가메 순미 대음양)
    #"https://www.saketime.jp/brands/997", #도쿄 - 이케부쿠로 서점 기쿠히메 가양국화주
    #"https://www.saketime.jp/brands/525", #이케부쿠로 서점 - 秩父錦 치치부 니시키
    #"https://www.saketime.jp/brands/297", #이케부쿠로 - 大七 極上生もと限定醸造吟醸 다이시치 극상생 어쩌고
    #"https://www.saketime.jp/brands/995", # 도쿄 긴자점 - 加賀鳶 純大吟 千日囲い錦絵 720ML 카가토비 준다이긴 어쩌고
    #"https://www.saketime.jp/brands/990", # 도쿄 긴자점 - 天狗舞 山廃純米大吟醸 720ML Tengu Mai 어쩌고
    #"https://www.saketime.jp/brands/176", # 도쿄 긴자점 - 浦霞 純米酒 720ML Ura Kasumi
    #"https://www.saketime.jp/brands/1404", # 도쿄 진자 - 松竹梅 上撰 1.8L 2 개 판지 포장
    #"https://www.saketime.jp/brands/1001",
    "https://www.saketime.jp/brands/298"
]

for url in urls:
    # 해당 URL로 이동
    driver.get(url)

    # 페이지 로드 대기 (필요 시 추가)
    driver.implicitly_wait(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 요소를 선택하고 텍스트를 추출합니다.

    #------술 이름-------#
    title_element = soup.select_one("h1")
    if title_element is not None:
        title = title_element.text.strip().replace(' ', '')
        # 번역
        title = translator.translate(title, src='ja', dest='ko').text
    else:
        title = "설명을 찾을 수 없습니다."

    #-----맛 설명-----#
    explain_element = soup.select_one(".mod-subsection.mod-centerbox > p")
    if explain_element is not None:
        explain = explain_element.text.strip()
        # 번역
        explain = translator.translate(explain, src='ja', dest='ko').text
    else:
        explain = "설명을 찾을 수 없습니다."

    #----리뷰 텍스트, 날짜, 작성자, 별점-----#
    reviews = []
    dates = []
    writers = []
    scores = []

    items = soup.select("li.wrap.clearfix")
    for i, item in enumerate(items):
        if i >= 10:
            break
        review_element = item.select_one(".r-text > p.r-body")
        if review_element is not None:
            review = review_element.text.strip().replace('\n', '').replace(' ','')
            # 번역
            translated_review = ""
            for start_index in range(0, len(review), 5000):
                chunk = review[start_index:start_index+5000]
                translated_chunk = translator.translate(chunk, src='ja', dest='ko').text
                translated_review += translated_chunk + " "
            reviews.append(translated_review.strip())
        else:
            reviews.append("리뷰를 찾을 수 없습니다.")

        #------날짜-------#
        day_element = item.select_one("p.r-date")
        if day_element is not None:
            day = day_element.text.strip()
            # 번역
            translated_day = translator.translate(day, src='ja', dest='ko').text
            dates.append(translated_day)
        else:
            dates.append("설명을 찾을 수 없습니다.")

        #------작성자------#
        writer_element = item.select_one("h3")
        if writer_element is not None:
            writer = writer_element.text.strip()
            # 번역
            translated_writer = translator.translate(writer, src='ja', dest='ko').text
            writers.append(translated_writer)
        else:
            writers.append("찾을 수 없습니다")

        #-------별점-------#
        score_element = item.select_one(".score")
        if score_element is not None:
            score = score_element.get("data-score")
            scores.append(score)
        else:
            scores.append("찾을 수 없습니다")

    # 출력
    print(f"이름: {title}")
    for idx, (review, date, writer, score) in enumerate(zip(reviews, dates, writers, scores), 1):
        print(f"작성자: {writer}")
        print(f"리뷰 {idx}: {review} ")
        print(f"작성 날짜: {date}")
        print(f"별점: {score}\n")

    # 데이터베이스에 저장
    save_data_to_mysql(title, explain, reviews, dates, writers, scores)

# 크롤링 완료 후 드라이버 종료
driver.quit()