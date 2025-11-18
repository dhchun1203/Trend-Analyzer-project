from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from db.mongo import collection

def crawl_naver_best100_fixed():
    print("🚀 네이버 베스트 100 크롤링 시작 (수정된 버전)")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 여러 URL 시도
        urls_to_try = [
            "https://shopping.naver.com/best100v2/main.naver",
            "https://shopping.naver.com/best100",
            "https://shopping.naver.com/best100v2"
        ]
        
        data_list = []
        
        for url in urls_to_try:
            print(f"🔍 URL 시도: {url}")
            driver.get(url)
            
            # 페이지 로딩 대기
            time.sleep(5)
            
            # JavaScript 실행 대기
            try:
                wait = WebDriverWait(driver, 15)
                # 상품 관련 요소가 나타날 때까지 대기
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='product'], [class*='best'], [class*='item']")))
                print("✅ 페이지 로딩 완료")
            except Exception as e:
                print(f"⚠️ 대기 시간 초과: {e}")
                continue
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            print(f"📄 HTML 길이: {len(driver.page_source)}")
            
            # 다양한 선택자 시도
            selectors_to_try = [
                "li.simpleBestProductCardResponsive_simple_best_product_card_responsive__GPB5o",
                "li[class*='best_product']",
                "li[class*='product']",
                "div[class*='best_product']",
                "div[class*='product']",
                "[class*='best'] [class*='product']",
                "[class*='product'] [class*='item']",
                ".product_item",
                ".best_item",
                "li",  # 모든 li 요소
                "div"   # 모든 div 요소
            ]
            
            products = []
            for selector in selectors_to_try:
                products = soup.select(selector)
                if len(products) > 0:
                    print(f"✅ 선택자 '{selector}'로 {len(products)}개 요소 발견!")
                    break
            
            if len(products) > 0:
                print(f"🎯 상품 데이터 추출 시작 (총 {len(products)}개)")
                
                for i, product in enumerate(products[:100], 1):
                    try:
                        # 이미지 및 상품명
                        img_tag = product.select_one("img")
                        title = img_tag.get("alt", "") if img_tag else "상품명 없음"
                        image_url = img_tag.get("src", "") if img_tag else ""
                        
                        # 상품 링크
                        link_tag = product.select_one("a")
                        link = link_tag.get("href", "") if link_tag else ""
                        
                        # 가격 (다양한 선택자 시도)
                        price = "가격 없음"
                        price_selectors = [
                            "[class*='price']",
                            "[class*='cost']",
                            "[class*='amount']",
                            "span",
                            "div"
                        ]
                        
                        for price_selector in price_selectors:
                            price_tag = product.select_one(price_selector)
                            if price_tag and price_tag.text.strip():
                                price_text = price_tag.text.strip()
                                if any(char.isdigit() for char in price_text):
                                    price = price_text
                                    break
                        
                        # 상품 정보가 충분한 경우만 추가
                        if title and title != "상품명 없음":
                            item = {
                                "rank": i,
                                "product_name": title,
                                "price": price,
                                "product_url": link,
                                "image_url": image_url,
                                "mall_name": "",  # 필요시 추가 분석
                                "category": "전체"
                            }
                            data_list.append(item)
                            print(f"   {i}. {title[:30]}... - {price}")
                    
                    except Exception as e:
                        print(f"   ⚠️ 상품 {i} 처리 중 오류: {e}")
                        continue
                
                if data_list:
                    print(f"🎉 총 {len(data_list)}개 상품 데이터 추출 완료!")
                    break
            else:
                print(f"❌ URL {url}에서 상품을 찾을 수 없음")
                continue
        
        # MongoDB 저장
        if data_list:
            try:
                collection.delete_many({"category": "전체"})
                collection.insert_many(data_list)
                print(f"💾 MongoDB에 {len(data_list)}개 상품 저장 완료!")
            except Exception as e:
                print(f"⚠️ MongoDB 저장 실패: {e}")
        else:
            print("❌ 추출된 상품 데이터가 없습니다")
        
        return data_list
        
    except Exception as e:
        print(f"❌ 크롤링 중 오류 발생: {e}")
        return []
    
    finally:
        driver.quit()
        print("🏁 크롤링 완료")

if __name__ == "__main__":
    result = crawl_naver_best100_fixed()
    print(f"📊 최종 결과: {len(result)}개 상품") 