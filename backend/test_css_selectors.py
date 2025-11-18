from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def test_css_selectors():
    print("🔍 네이버 베스트 100 CSS 선택자 테스트 시작...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://shopping.naver.com/best100v2/main.naver"
        print(f"📱 URL 접속: {url}")
        driver.get(url)
        time.sleep(5)  # 페이지 로딩 대기

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # 1. 상품 카드 선택자 테스트
        print("\n1️⃣ 상품 카드 선택자 테스트:")
        products = soup.select("li.simpleBestProductCardResponsive_simple_best_product_card_responsive__GPB5o")
        print(f"   - 상품 카드 개수: {len(products)}")
        
        if len(products) == 0:
            print("   ❌ 상품 카드를 찾을 수 없습니다!")
            print("   🔍 대안 선택자 찾기...")
            
            # 대안 선택자들 시도
            alternative_selectors = [
                "li[class*='best_product']",
                "li[class*='product']",
                "div[class*='best_product']",
                "div[class*='product']",
                ".product_item",
                ".best_item"
            ]
            
            for selector in alternative_selectors:
                alt_products = soup.select(selector)
                if len(alt_products) > 0:
                    print(f"   ✅ 대안 선택자 '{selector}'로 {len(alt_products)}개 상품 발견!")
                    break
        
        # 2. 첫 번째 상품에서 세부 선택자 테스트
        if len(products) > 0:
            print("\n2️⃣ 첫 번째 상품 세부 선택자 테스트:")
            first_product = products[0]
            
            # 이미지 테스트
            img_tag = first_product.select_one("img.simpleBestProductCardResponsive_image__krLZN")
            if img_tag:
                print(f"   ✅ 이미지 선택자: {img_tag.get('alt', '제목 없음')}")
            else:
                print("   ❌ 이미지 선택자 실패")
                # 대안 이미지 선택자 시도
                alt_img = first_product.select_one("img")
                if alt_img:
                    print(f"   🔍 대안 이미지: {alt_img.get('alt', '제목 없음')}")
            
            # 링크 테스트
            link_tag = first_product.select_one("a.simpleBestProductCardResponsive_link__CPaQh")
            if link_tag:
                print(f"   ✅ 링크 선택자: {link_tag.get('href', '링크 없음')}")
            else:
                print("   ❌ 링크 선택자 실패")
                # 대안 링크 선택자 시도
                alt_link = first_product.select_one("a")
                if alt_link:
                    print(f"   🔍 대안 링크: {alt_link.get('href', '링크 없음')}")
            
            # 가격 테스트
            price_tag = first_product.select_one("div.simpleBestProductCardResponsive_origin_price__XjEwV")
            if price_tag:
                print(f"   ✅ 원가 선택자: {price_tag.text.strip()}")
            else:
                print("   ❌ 원가 선택자 실패")
                # 대안 가격 선택자 시도
                alt_price = first_product.select_one("[class*='price']")
                if alt_price:
                    print(f"   🔍 대안 가격: {alt_price.text.strip()}")
        
        # 3. 페이지 전체 HTML 구조 확인
        print("\n3️⃣ 페이지 구조 분석:")
        print(f"   - 전체 HTML 길이: {len(driver.page_source)}")
        
        # 클래스명에 'best'가 포함된 요소들 찾기
        best_elements = soup.find_all(class_=lambda x: x and 'best' in x.lower())
        print(f"   - 'best'가 포함된 클래스 개수: {len(best_elements)}")
        
        # 클래스명에 'product'가 포함된 요소들 찾기
        product_elements = soup.find_all(class_=lambda x: x and 'product' in x.lower())
        print(f"   - 'product'가 포함된 클래스 개수: {len(product_elements)}")
        
        if len(best_elements) > 0:
            print("   📋 'best' 클래스 예시:")
            for i, elem in enumerate(best_elements[:5]):
                print(f"      {i+1}. {elem.get('class', [])}")
        
        if len(product_elements) > 0:
            print("   📋 'product' 클래스 예시:")
            for i, elem in enumerate(product_elements[:5]):
                print(f"      {i+1}. {elem.get('class', [])}")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
    
    finally:
        driver.quit()
        print("\n🏁 테스트 완료")

if __name__ == "__main__":
    test_css_selectors() 