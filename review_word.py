from selenium import webdriver
from bs4 import BeautifulSoup
from googletrans import Translator
import os
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import requests
import mysql.connector

# 구글 번역 객체 생성
translator = Translator()

# 형태소 분석기 설정
okt = Okt()

def extract_keywords(text):
    # 형태소 분석을 통해 형용사, 부사, 명사, 동사 추출
    keywords = []
    for word, pos in okt.pos(text):
        if pos in ['Adjective', 'Adverb', 'Noun', 'Verb']:  # 형용사, 부사, 명사, 동사 추출
            keywords.append(word)
    return keywords

# 불용어 설정
stop_words = {'입니다', '있습니다', '없습니다', '홍', '치', '년', '의해', '또는', '합', '나', '수', '도', '우', '없었습니까', 
              '갓', '탭', '이번', '바', '베', '웨어', '바빠서', '때', '입', '만', '실은', '스럽다고', '실', '산', '위', 
              '및', '같은', '따라서', '것', '무엇', '오늘', '이', '그것', '키', '의', '약간', '맛', '임', '뇨', '엽', '니', 
              '월경', '내', '약', '후', '다른', '더', '과', '움', '가슴', '때문', '롭습니', '쌀', '로서', '술', '매우', '날', 
              '번', '느낌', '병', '주류', '생각', '노화', '실온', '온도', '작년', '알코올', '인상', '혼자', '몸', '첫날', '두', 
              '폐기물', '증가', '가장', '추위', '산이', '를', '생', '월', '위해', '마다', '만듭니', '중', '키쿠', '준비', 
              '사용', '유마미', '집', '우마미', '색상', '사용','할','있지만','된','됩니다','세트','비교','와','폐지',
              '지원','재건','느꼈지만','풍','마시고','합니다','는','있는','들었습니다','오는','버려진','않은','가격','댄스','기장',
              '마시면','와','배웠던','띄지','했습니다','합니다','됩니다','는','너무','좋은','구입','왁스','느낍니다','올해','미야기','거의','사람','쉽습니다',
              '납니다','카사','당신','비정상','구입','향기','한','할','는','치치','있지만','사이타마','얻었다','라인','가격',
              '당신','않습니다','했습니다','세금','길가','하는','했다','제한','옳습니다','카','할','잔','적','된','되고',
              '좀더','히','손님','옆테','싶었','나고','스프레드','마셨다','슺','시티','이루었습니다','와','합니다','동안','여전히',
              '엽다','아니요','합니다','여전히','하는','있지만','않지만','하지','결국','나이','습니다','사양','추가','사고','너무','노란색','전적','엔',
              '검은','든','했기','빨간색','하임','느끼지','같습니다','양조장','효모','와인','목구멍','펼쳐진','잘','될','색','게시','그렇게','말','하여','은',
              '야마다','전통','마시기','확실히','평평한','슺다','없는','있으며','음식','추워요','대었습니다','구매','대나무',
              '분명히','양조','감자','따르면','그래','목적지','보입니다','즉시','싶습니다','면','좋아하지','주요','제조업체','가지','끔','기술','마실','갈','예상',
              '요구','술어','해야','주석','없고','현대','일','포함','처음','십','농업','이시카와','펀치','사케','붉은','공장','벽돌','돌아','남자','하면','오래된',
              '진조','이미지','오랫동안','갤러리','선명한','뒤','합리','상점','함께','왔습니다','때리는','낫습'}



#Imgur API 설정
IMGUR_CLIENT_ID = 'cb98825be38c965' #클라이언트 아이디 설정

def upload_image_to_imgur(image_path):
    headers = {
        'Authorization' : f'Client-ID {IMGUR_CLIENT_ID}'
    }
    url = "https://api.imgur.com/3/upload"
    with open(image_path, 'rb') as image_file:
        response = requests.post(url, headers=headers, files={'image': image_file})
    data = response.json()
    return data['data']['link']


# # # MySQL 연결 설정
# db_config = {
#     'user': 'admin',
#     'password': 'tkzptkzptkrp24',
#     'host': 'database-sakesage.c3suqkcwcjd4.ap-northeast-2.rds.amazonaws.com',
#     'database': 'sakesage'
# }

# # MySQL에 데이터 저장 함수
# def save_data_to_mysql(title, imgur_url):
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#         # 데이터 삽입
#         query = "INSERT INTO review_images (name, imgur_url) VALUES (%s, %s)"
#         cursor.execute(query, (title, imgur_url))
#         conn.commit()
#         print("데이터가 MySQL에 저장되었습니다.")
#     except mysql.connector.Error as error:
#         print(f"MySQL 에러: {error}")
#     finally:
#         cursor.close()
#         conn.close()



# 웹 드라이버 설정
driver = webdriver.Chrome()  # 크롬 드라이버 경로 설정 필요

# 현재 작업 디렉토리의 경로를 가져옴
current_dir = os.getcwd()

# 이미지를 저장할 폴더 경로 생성
image_folder = os.path.join(current_dir, "wordcloud_images")

# 이미지를 저장할 폴더 생성
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# 여러 URL에 대해 순차적으로 크롤링
urls = [
    #"https://www.saketime.jp/brands/696/page:{}", 
    #"https://www.saketime.jp/brands/997/page:{}", 
    #"https://www.saketime.jp/brands/525/page:{}", 
    #"https://www.saketime.jp/brands/297/page:{}", 
    #"https://www.saketime.jp/brands/995/page:{}", 
    #"https://www.saketime.jp/brands/990/page:{}", 
    #"https://www.saketime.jp/brands/176/page:{}",
    #"https://www.saketime.jp/brands/1404/page:{}",
    #"https://www.saketime.jp/brands/1001/page:{}",
    "https://www.saketime.jp/brands/298/page:{}"
]

for base_url in urls:
    all_reviews = []
    all_review_keywords = []
    for page_num in range(1, 6): # 페이지 번호 1에서 5까지
        url = base_url.format(page_num)
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
            # 키워드 추출
            explain_keywords = extract_keywords(explain)
        else:
            explain = "설명을 찾을 수 없습니다."
            explain_keywords = []

        #----리뷰 텍스트, 날짜, 작성자, 별점-----#
        items = soup.select("li.wrap.clearfix")
        for item in items:
            review_element = item.select_one(".r-text > p.r-body")
            if review_element is not None:
                review = review_element.text.strip().replace('\n', '').replace(' ','')
                # 번역
                translated_review = ""
                for start_index in range(0, len(review), 5000):
                    chunk = review[start_index:start_index+5000]
                    translated_chunk = translator.translate(chunk, src='ja', dest='ko').text
                    translated_review += translated_chunk + " "
                translated_review = translated_review.strip()
                all_reviews.append(translated_review)

                # 키워드 추출
                review_keywords = [word for word in extract_keywords(translated_review) if word not in stop_words]
                all_review_keywords.append(review_keywords)

                # 30개의 리뷰를 수집하면 중지
                if len(all_reviews) >= 30:
                    break

        # 30개의 리뷰를 수집하면 중지
        if len(all_reviews) >= 30:
            break

        # 출력
        #print(f"이름: {title}")

        # 리뷰 키워드들을 하나의 리스트로 합침
        all_keywords = [keyword for sublist in all_review_keywords for keyword in sublist]  # 리스트 평탄화

        # 각 키워드의 빈도수 계산
        keyword_counter = Counter(all_keywords)

        # 워드클라우드 생성
        wordcloud = WordCloud(font_path='/Library/Fonts/NanumGothic.ttf',
                        width=800, height=800,
                        background_color='white')
        wordcloud.generate_from_frequencies(keyword_counter)

        # 이미지 파일 경로 설정
        image_file_path = os.path.join(image_folder, f"{title}.png")

        # 워드클라우드 이미지를 파일로 저장
        wordcloud.to_file(image_file_path)

         # Imgur에 이미지 업로드
        imgur_url = upload_image_to_imgur(image_file_path)
        # 업로드된 이미지의 URL 출력
        print(f"{title}이미지가 성공적으로 업로드되었습니다. URL: {imgur_url}")

        # MySQL에 이미지 URL 저장
        #save_data_to_mysql(title, imgur_url)

        # 워드클라우드 이미지를 화면에 출력
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

        for idx, review_keywords in enumerate(all_review_keywords, 1):
            print(f"리뷰 {idx}: {review_keywords} \n")

# 크롤링 완료 후 드라이버 종료
driver.quit()
