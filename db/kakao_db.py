import time
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

print("유령 브라우저 (심층 타격 모드) 시동 중...")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

query = "강남구 치과"
driver.get(f"https://map.kakao.com/?q={query}")
time.sleep(4) 

filename = f"강남구_치과_심층DB_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
# 엑셀 헤더에 평점, 리뷰수, 홈페이지 추가
writer.writerow(['상호명', '전화번호', '주소', '평점', '리뷰수', '홈페이지']) 

count = 0

# 1. '장소 더보기' 버튼 강제 클릭 (숨김 해제)
try:
    more_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "info.search.place.more"))
    )
    driver.execute_script("arguments[0].click();", more_btn)
    time.sleep(3) 
except:
    pass

page = 1
while True:
    print(f"--- {page}페이지 심층 타격 중 ---")
    time.sleep(2)
    
    # 2. 현재 화면의 HTML을 통째로 떠서 BeautifulSoup으로 초고속 핀셋 추출
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    places = soup.find_all("li", class_="PlaceItem")
    
    for place in places:
        try:
            # 기본 정보 추출
            name = place.find("a", class_="link_name").text.strip()
            phone_tag = place.find("span", class_="phone")
            phone = phone_tag.text.strip() if phone_tag else ""
            
            addr_tag = place.find("div", class_="addr")
            addr = addr_tag.find("p").text.strip() if addr_tag else ""
            
            if not name or not phone:
                continue
                
            # 심층 정보 추출 (평점, 리뷰, 홈페이지)
            rating_tag = place.find("em", class_="num")
            rating = rating_tag.text.strip() if rating_tag else "0"
            
            review_tag = place.find("a", class_="numberof_review")
            review_count = review_tag.text.strip() if review_tag else "0"
            
            homepage_tag = place.find("a", class_="homepage")
            homepage = homepage_tag.get("href") if homepage_tag else "없음"
            
            writer.writerow([name, phone, addr, rating, review_count, homepage])
            count += 1
            
        except Exception as e:
            continue

    # 3. 페이지 넘기기
    try:
        if page % 5 == 0:
            next_btn = driver.find_element(By.ID, "info.search.page.next")
            if "disabled" in next_btn.get_attribute("class"):
                break 
            driver.execute_script("arguments[0].click();", next_btn)
        else:
            next_page_num = (page % 5) + 1
            page_btn = driver.find_element(By.ID, f"info.search.page.no{next_page_num}")
            if "hidden" in page_btn.get_attribute("class"):
                break 
            driver.execute_script("arguments[0].click();", page_btn)
        page += 1
    except:
        break

driver.quit()
f.close()
print(f"\n[작전 완료] 관악구 치과 심층 DB 총 {count}개 싹쓸이 완료! 파일명: {filename}")
