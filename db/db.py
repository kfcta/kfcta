import requests
from bs4 import BeautifulSoup
import csv
import datetime

# 1. 타격 목표 설정
query = "K-푸드 수출"
url = f"https://search.naver.com/search.naver?where=news&query={query}"

# 2. 봇 차단 회피 (사람인 척 위장)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.0.0 Safari/537.36"}

print(f"[{query}] 네이버 뉴스 타격 시작...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 3. 뉴스 기사 제목과 링크 긁어오기 (네이버 뉴스 HTML 구조)
articles = soup.find_all('a', {'class': 'news_tit'})

# 4. 추출한 데이터를 엑셀(CSV)로 저장
filename = f"K-Food_뉴스_DB_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['순번', '기사 제목', 'URL 링크'])
    
    for idx, article in enumerate(articles, 1):
        title = article.get('title')
        link = article.get('href')
        writer.writerow([idx, title, link])
        print(f"{idx}. {title}")

print(f"\n[작전 완료] 같은 폴더에 '{filename}' 파일이 생성되었습니다.")
