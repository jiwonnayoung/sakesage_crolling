from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')

# 웹 드라이버 설정
driver = webdriver.Chrome(options=chrome_options)

# 여러 URL에 대해 순차적으로 크롤링
urls = [
    "https://sakurajapan.co.kr/deal/detail?url=https://item.rakuten.co.jp/ledled/3-glengrant-10/&shop_id=rakuten&lo=",#글렌 그란트 10년 グレングラント10年 (도쿄 -긴자)
    "https://sakurajapan.co.kr/deal/detail?url=https://item.rakuten.co.jp/ledled/3-dalmore-12y/&shop_id=rakuten&lo=", #달모어 12년 ダルモア１２年 (도쿄 - 긴자) - dalmore 12 
    "https://sakurajapan.co.kr/deal/detail?url=https://item.rakuten.co.jp/ledled/3-glngyn-10y/&shop_id=rakuten&lo=", #글렌 고인 10년 700ML グレンゴイン10年 (도쿄 - 긴자) glengoyne 10 years
    "https://sakurajapan.co.kr/deal/detail?url=https://item.rakuten.co.jp/liquorsbest/101203601/&shop_id=rakuten&lo=" , #발렌타인 17년 バランタイン17年 750ml(箱無)ballantine 17 years
    "https://sakurajapan.co.kr/deal/detail?url=https://item.rakuten.co.jp/whisky/514799/&shop_id=rakuten&lo=", #글렌그란트 아보랄리스, 알보랄리스
]

for url in urls:
    # 해당 URL로 이동
    driver.get(url)

    # 페이지 로드 대기 (필요 시 추가)
    time.sleep(10)  # 페이지가 완전히 로드될 시간을 줍니다

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #------술 이름-------#
    title_element = soup.select_one(".pro_d_tit")
    if title_element is not None:
        title = title_element.text.strip().replace(' ', '')
    else:
        title = "설명을 찾을 수 없습니다."

    #----리뷰 텍스트, 날짜, 작성자-----#
    reviews = []
    dates = []
    writers = []

    items = soup.select("ul > li")
    
    for i, item in enumerate(items, start=1):
        # if i >= 5:
        #     break
        #------리뷰 텍스트-------#
        review_element = item.select_one("span.de_in_text")
        if review_element is not None:
            review = review_element.text.strip().replace('\n', '')
            reviews.append(review.strip())
        else:
            reviews.append("리뷰를 찾을 수 없습니다.")

        #------날짜-------#
        day_element = item.select_one(".tit_date")
        if day_element is not None:
            day = day_element.text.strip()
            dates.append(day)
        else:
            dates.append("날짜를 찾을 수 없습니다.")

        #------작성자------#
        writer_element = item.select_one(".tit_name")
        if writer_element is not None:
            writer = writer_element.text.strip()
            writers.append(writer)
        else:
            writers.append("작성자를 찾을 수 없습니다")

    # 출력
    print(f"이름: {title}")
    for idx, (review, date, writer) in enumerate(zip(reviews, dates, writers), start=1):
        print(f"작성자: {writer}")
        print(f"리뷰 {idx}: {review}")
        print(f"작성 날짜: {date}")
    
# 웹 드라이버 종료
driver.quit()
