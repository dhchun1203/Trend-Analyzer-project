from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from db.mongo import collection
    MONGODB_AVAILABLE = True
    print("✅ MongoDB 연결 성공")
except ImportError:
    MONGODB_AVAILABLE = False
    print("⚠️ MongoDB 연결 실패 - 데이터만 출력합니다")

def crawl_naver_best100_advanced():
    print("🚀 네이버 베스트 100 크롤링 시작 (고급 버전)")
    
    options = webdriver.ChromeOptions()
    # 헤드리스 모드 비활성화 (디버깅용)
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 자동화 감지 방지
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # 메인 URL로 접속
        url = "https://shopping.naver.com/best100v2/main.naver"
        print(f"🔍 URL 접속: {url}")
        driver.get(url)
        
        # 충분한 로딩 시간 대기
        print("⏳ 페이지 로딩 대기 중...")
        time.sleep(10)
        
        # 페이지 스크롤 (동적 콘텐츠 로딩 유도)
        print("📜 페이지 스크롤 중...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # 현재 페이지 상태 확인
        page_source = driver.page_source
        print(f"📄 HTML 길이: {len(page_source)}")
        
        # HTML 내용 일부 출력 (디버깅용)
        print("🔍 HTML 내용 일부:")
        print(page_source[:1000])
        
        soup = BeautifulSoup(page_source, "html.parser")
        
        # 1. 모든 이미지 태그 찾기
        all_images = soup.find_all("img")
        print(f"📸 전체 이미지 개수: {len(all_images)}")
        
        # 2. 모든 링크 태그 찾기
        all_links = soup.find_all("a")
        print(f"🔗 전체 링크 개수: {len(all_links)}")
        
        # 3. 상품 관련 텍스트가 포함된 요소들 찾기
        product_keywords = ["상품", "제품", "가격", "원", "₩", "구매", "장바구니", "찜"]
        product_elements = []
        
        for keyword in product_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            if elements:
                product_elements.extend(elements)
        
        print(f"🛍️ 상품 관련 텍스트 요소 개수: {len(product_elements)}")
        
        # 4. 숫자와 원화 기호가 포함된 텍스트 찾기 (가격 정보)
        price_pattern = re.compile(r'[\d,]+원')
        price_elements = soup.find_all(text=price_pattern)
        print(f"💰 가격 정보 요소 개수: {len(price_elements)}")
        
        # 5. 실제 상품 데이터 추출 시도
        data_list = []
        
        # 방법 1: 이미지와 링크가 있는 요소들 찾기
        print("\n🎯 방법 1: 이미지+링크 조합으로 상품 찾기")
        for i, img in enumerate(all_images[:50]):  # 처음 50개만 시도
            try:
                # 이미지 주변의 링크 찾기
                parent = img.parent
                link_tag = None
                
                # 부모 요소에서 링크 찾기
                for _ in range(5):  # 최대 5단계 상위로 검색
                    if parent:
                        link_tag = parent.find("a")
                        if link_tag:
                            break
                        parent = parent.parent
                
                if link_tag and img.get("alt"):
                    title = img.get("alt", "").strip()
                    image_url = img.get("src", "")
                    link = link_tag.get("href", "")
                    
                    # 가격 정보 찾기
                    price = "가격 없음"
                    price_parent = img.parent
                    for _ in range(3):
                        if price_parent:
                            price_text = price_parent.get_text()
                            price_match = price_pattern.search(price_text)
                            if price_match:
                                price = price_match.group()
                                break
                            price_parent = price_parent.parent
                    
                    if title and len(title) > 2:  # 의미있는 제목인 경우만
                        item = {
                            "rank": i + 1,
                            "product_name": title,
                            "price": price,
                            "product_url": link,
                            "image_url": image_url,
                            "mall_name": "",
                            "category": "전체"
                        }
                        data_list.append(item)
                        print(f"   {i+1}. {title[:30]}... - {price}")
                
            except Exception as e:
                continue
        
        # 방법 2: 링크가 있는 요소들에서 상품 정보 추출
        if len(data_list) < 10:
            print("\n🎯 방법 2: 링크 기반으로 상품 찾기")
            for i, link in enumerate(all_links[:100]):
                try:
                    link_text = link.get_text().strip()
                    link_href = link.get("href", "")
                    
                    # 상품 링크인지 확인 (shopping.naver.com 포함)
                    if "shopping.naver.com" in link_href and link_text:
                        # 링크 주변의 이미지 찾기
                        img_tag = link.find("img")
                        title = img_tag.get("alt", "") if img_tag else link_text
                        image_url = img_tag.get("src", "") if img_tag else ""
                        
                        # 가격 정보 찾기
                        price = "가격 없음"
                        price_text = link.get_text()
                        price_match = price_pattern.search(price_text)
                        if price_match:
                            price = price_match.group()
                        
                        if title and len(title) > 2:
                            item = {
                                "rank": len(data_list) + 1,
                                "product_name": title,
                                "price": price,
                                "product_url": link_href,
                                "image_url": image_url,
                                "mall_name": "",
                                "category": "전체"
                            }
                            data_list.append(item)
                            print(f"   {len(data_list)}. {title[:30]}... - {price}")
                
                except Exception as e:
                    continue
        
        # 6. 결과 정리
        print(f"\n📊 총 {len(data_list)}개 상품 데이터 추출 완료!")
        
        # 7. MongoDB 저장 (가능한 경우에만)
        if data_list and MONGODB_AVAILABLE:
            try:
                collection.delete_many({"category": "전체"})
                collection.insert_many(data_list)
                print(f"💾 MongoDB에 {len(data_list)}개 상품 저장 완료!")
            except Exception as e:
                print(f"⚠️ MongoDB 저장 실패: {e}")
        elif data_list:
            print("💾 MongoDB 연결 불가 - 데이터만 출력합니다")
            for item in data_list[:5]:  # 처음 5개만 출력
                print(f"   📦 {item['rank']}. {item['product_name'][:30]}... - {item['price']}")
        else:
            print("❌ 추출된 상품 데이터가 없습니다")
            print("🔍 페이지 구조를 다시 분석해야 할 수 있습니다")
        
        return data_list
        
    except Exception as e:
        print(f"❌ 크롤링 중 오류 발생: {e}")
        return []
    
    finally:
        driver.quit()
        print("🏁 크롤링 완료")

if __name__ == "__main__":
    result = crawl_naver_best100_advanced()
    print(f"📊 최종 결과: {len(result)}개 상품") 