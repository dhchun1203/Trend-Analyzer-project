from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from db.mongo import collection, MONGODB_AVAILABLE

def crawl_naver_best100():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://shopping.naver.com/best100v2/main.naver"
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.select("li.simpleBestProductCardResponsive_simple_best_product_card_responsive__GPB5o")

    data_list = []
    for i, product in enumerate(products[:100], 1):
        # 이미지 및 상품명
        img_tag = product.select_one("img.simpleBestProductCardResponsive_image__krLZN")
        title = img_tag["alt"] if img_tag else "상품명 없음"
        image_url = img_tag["src"] if img_tag else ""

        # 상품 링크
        link_tag = product.select_one("a.simpleBestProductCardResponsive_link__CPaQh")
        link = link_tag["href"] if link_tag else ""

        # 가격
        price_tag = product.select_one("div.simpleBestProductCardResponsive_origin_price__XjEwV")
        price = price_tag.text.strip() if price_tag else "가격 없음"

        # 할인 가격(있으면)
        discount_tag = product.select_one("div.simpleBestProductCardResponsive_discount_price__1WgDd")
        if discount_tag:
            price = discount_tag.text.strip()

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

    # MongoDB 저장 (연결된 경우에만)
    if data_list and MONGODB_AVAILABLE and collection is not None:
        try:
            collection.delete_many({"category": "전체"})
            collection.insert_many(data_list)
            print(f"💾 MongoDB에 {len(data_list)}개 상품 저장 완료!")
        except Exception as e:
            print(f"⚠️ MongoDB 저장 실패: {e}")

    driver.quit()
    return data_list
