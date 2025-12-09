from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from crawler.naver_best100 import crawl_naver_best100
from db.mongo import collection, MONGODB_AVAILABLE
from bson import ObjectId
from naver_auth import NaverAdAuth
from naver_keyword_api import NaverKeywordAPI
from naver_datalab_api import NaverDatalabAPI
from naver_search_api import NaverSearchAPI
import os

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 로컬 개발 환경
        "https://dhchun1203.github.io",  # GitHub Pages 도메인
        "https://*.github.io",  # 모든 GitHub Pages 서브도메인
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 네이버 광고 API 인증 객체
naver_auth = NaverAdAuth()
naver_keyword_api = NaverKeywordAPI()
naver_datalab_api = NaverDatalabAPI()
naver_search_api = NaverSearchAPI()

def convert_objectid(obj):
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

@app.get("/items")
def get_items():
    if not MONGODB_AVAILABLE or collection is None:
        raise HTTPException(status_code=503, detail="MongoDB가 연결되지 않았습니다.")
    data = list(collection.find({"category": "전체"}))
    data = [convert_objectid(doc) for doc in data]
    return {"items": data, "count": len(data)}

@app.get("/crawl")
def get_best100():
    """인기 키워드 기반 상품 검색 API (크롤링 대체)"""
    try:
        # 인기 키워드 리스트
        popular_keywords = [
            "로봇청소기", "에어프라이어", "공기청정기", "커피머신", "전자레인지",
            "청소기", "선풍기", "가습기", "제습기", "온풍기",
            "전기밥솥", "믹서기", "블렌더", "토스터", "전기포트",
            "다리미", "건조기", "세탁기", "냉장고", "TV"
        ]
        
        all_products = []
        
        for keyword in popular_keywords:
            try:
                # 각 키워드로 쇼핑 검색
                result = naver_search_api.search_shopping(keyword, 5)  # 각 키워드당 5개
                if 'items' in result and result['items']:
                    for i, item in enumerate(result['items']):
                        # 상품 정보 정리
                        product = {
                            "rank": len(all_products) + 1,
                            "product_name": item.get('title', '').replace('<b>', '').replace('</b>', ''),
                            "price": item.get('lprice', '가격 정보 없음'),
                            "product_url": item.get('link', ''),
                            "image_url": item.get('image', ''),
                            "mall_name": item.get('mallName', ''),
                            "category": "인기상품",
                            "keyword": keyword  # 어떤 키워드로 검색된 상품인지 표시
                        }
                        all_products.append(product)
                        
                        # 최대 100개까지만 수집
                        if len(all_products) >= 100:
                            break
                
                if len(all_products) >= 100:
                    break
                    
            except Exception as e:
                print(f"키워드 '{keyword}' 검색 중 오류: {e}")
                continue
        
        # MongoDB 저장 (연결된 경우에만)
        if all_products and MONGODB_AVAILABLE and collection is not None:
            try:
                collection.delete_many({"category": "인기상품"})
                collection.insert_many(all_products)
                print(f"💾 MongoDB에 {len(all_products)}개 인기상품 저장 완료!")
            except Exception as e:
                print(f"⚠️ MongoDB 저장 실패: {e}")
        
        return {"items": all_products, "count": len(all_products)}
        
    except Exception as e:
        print(f"❌ 인기상품 검색 중 오류: {e}")
        raise HTTPException(status_code=500, detail=f"상품 검색 실패: {str(e)}")

@app.get("/debug")
def debug_info():
    if not MONGODB_AVAILABLE or collection is None:
        return {
            "mongodb_available": False,
            "message": "MongoDB가 연결되지 않았습니다."
        }
    total_count = collection.count_documents({})
    category_count = collection.count_documents({"category": "전체"})
    all_data = list(collection.find({}).limit(5))
    all_data = [convert_objectid(doc) for doc in all_data]
    
    return {
        "mongodb_available": True,
        "total_documents": total_count,
        "category_documents": category_count,
        "sample_data": all_data
    }

# 네이버 광고 API 인증 관련 엔드포인트
@app.get("/auth/naver")
def start_naver_auth():
    """네이버 광고 API 인증 시작"""
    try:
        auth_url = naver_auth.generate_auth_url()
        return {"auth_url": auth_url, "message": "브라우저에서 위 URL로 접속하여 인증을 완료하세요."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인증 URL 생성 실패: {str(e)}")

@app.post("/auth/token/direct")
def get_token_direct():
    """Client Credentials 방식으로 직접 Access Token 발급"""
    try:
        token_data = naver_auth.get_access_token_direct()
        naver_auth.save_token_to_env()
        
        return {
            "message": "토큰이 성공적으로 발급되었습니다!",
            "access_token": token_data.get('access_token'),
            "expires_in": token_data.get('expires_in'),
            "token_type": token_data.get('token_type')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"토큰 발급 실패: {str(e)}")

@app.get("/auth/callback")
def naver_auth_callback(code: str, state: str = None):
    """네이버 광고 API 인증 콜백"""
    try:
        # Authorization Code를 Access Token으로 교환
        token_data = naver_auth.exchange_code_for_token(code)
        
        # 토큰을 환경 변수로 저장
        naver_auth.save_token_to_env()
        
        return {
            "message": "인증이 완료되었습니다!",
            "access_token": token_data.get('access_token'),
            "expires_in": token_data.get('expires_in'),
            "token_type": token_data.get('token_type')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"토큰 발급 실패: {str(e)}")

@app.get("/auth/status")
def check_auth_status():
    """인증 상태 확인"""
    try:
        # 환경 변수에서 토큰 로드
        naver_auth.load_token_from_env()
        
        is_valid = naver_auth.is_token_valid()
        
        return {
            "is_authenticated": is_valid,
            "has_access_token": bool(naver_auth.access_token),
            "has_refresh_token": bool(naver_auth.refresh_token),
            "token_expires_at": naver_auth.token_expires_at
        }
    except Exception as e:
        return {
            "is_authenticated": False,
            "error": str(e)
        }

@app.post("/auth/refresh")
def refresh_token():
    """Access Token 갱신"""
    try:
        naver_auth.load_token_from_env()
        token_data = naver_auth.refresh_access_token()
        naver_auth.save_token_to_env()
        
        return {
            "message": "토큰이 갱신되었습니다.",
            "access_token": token_data.get('access_token'),
            "expires_in": token_data.get('expires_in')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"토큰 갱신 실패: {str(e)}")

@app.get("/auth/test")
def test_auth():
    """인증 테스트 - 실제 API 호출"""
    try:
        naver_auth.load_token_from_env()
        
        if not naver_auth.is_token_valid():
            raise Exception("유효한 Access Token이 없습니다.")
        
        # 간단한 API 호출 테스트 (실제 구현 시 수정 필요)
        headers = naver_auth.get_auth_headers("GET", "/keywordstool")
        
        return {
            "message": "인증이 정상적으로 작동합니다!",
            "headers_generated": bool(headers),
            "access_token_exists": bool(naver_auth.access_token)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인증 테스트 실패: {str(e)}")

# 네이버 키워드 분석 API 엔드포인트
@app.get("/api/keyword/analysis")
def get_keyword_analysis(keyword: str):
    """키워드 분석 API"""
    try:
        result = naver_keyword_api.get_keyword_analysis(keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 분석 실패: {str(e)}")

@app.get("/api/keyword/test")
def test_keyword_api():
    """키워드 API 연결 테스트"""
    try:
        result = naver_keyword_api.test_api_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 API 테스트 실패: {str(e)}")

@app.get("/api/keyword/ideas")
def get_keyword_ideas(keyword: str, show_detail: str = "1"):
    """키워드 아이디어 조회 API"""
    try:
        result = naver_keyword_api.get_keyword_ideas(keyword, show_detail)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 아이디어 조회 실패: {str(e)}")

# 네이버 데이터랩 API 엔드포인트
@app.get("/api/datalab/trend")
def get_trend_analysis(keyword: str):
    """네이버 데이터랩 트렌드 분석 API"""
    try:
        result = naver_datalab_api.get_keyword_analysis(keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"트렌드 분석 실패: {str(e)}")

@app.get("/api/datalab/related-keywords")
def get_related_keywords(keyword: str):
    """연관 키워드 조회 API (실제 API 우선)"""
    try:
        result = naver_datalab_api.get_related_keywords_real(keyword)
        return {"related_keywords": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"연관 키워드 조회 실패: {str(e)}")

@app.get("/api/datalab/search-volume")
def get_search_volume(keyword: str):
    """검색량 통계 조회 API (실제 API 우선)"""
    try:
        result = naver_datalab_api.get_search_volume_stats_real(keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색량 통계 조회 실패: {str(e)}")

@app.get("/api/datalab/trend-chart")
def get_trend_chart_data(keyword: str):
    """트렌드 차트 데이터 조회 API (실제 API 우선)"""
    try:
        result = naver_datalab_api.get_trend_chart_data_real(keyword)
        return {"chart_data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"트렌드 차트 데이터 조회 실패: {str(e)}")

@app.get("/api/datalab/test")
def test_datalab_api():
    """네이버 데이터랩 API 연결 테스트"""
    try:
        result = naver_datalab_api.test_api_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터랩 API 테스트 실패: {str(e)}")

# 네이버 블로그 검색 API 엔드포인트
@app.get("/api/search/blogs")
def search_blogs(keyword: str, display: int = 10):
    """네이버 블로그 검색 API"""
    try:
        result = naver_search_api.search_keyword(keyword, display)
        # 블로그만 필터링
        if 'items' in result:
            blog_items = []
            for item in result['items']:
                # 블로그 포스트 정보 정리
                blog_item = {
                    'title': item.get('title', '').replace('<b>', '').replace('</b>', ''),
                    'description': item.get('description', '').replace('<b>', '').replace('</b>', ''),
                    'bloggername': item.get('bloggername', ''),
                    'bloggerlink': item.get('bloggerlink', ''),
                    'postdate': item.get('postdate', ''),
                    'link': item.get('link', '')
                }
                blog_items.append(blog_item)
            
            return {
                'total': result.get('total', 0),
                'display': len(blog_items),
                'keyword': keyword,
                'blogs': blog_items
            }
        else:
            return {
                'total': 0,
                'display': 0,
                'keyword': keyword,
                'blogs': []
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"블로그 검색 실패: {str(e)}")

# 네이버 쇼핑 검색 API 엔드포인트
@app.get("/api/search/shopping")
def search_shopping(keyword: str, display: int = 20):
    """네이버 쇼핑 검색 API"""
    try:
        result = naver_search_api.search_shopping(keyword, display)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"쇼핑 검색 실패: {str(e)}")

# 쇼핑 특화 연관 키워드 API 엔드포인트
@app.get("/api/keyword/shopping-related")
def get_shopping_related_keywords(keyword: str):
    """쇼핑에 특화된 연관 키워드 조회 API"""
    try:
        result = naver_search_api.get_shopping_related_keywords(keyword)
        return {"related_keywords": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"쇼핑 연관 키워드 조회 실패: {str(e)}")

@app.get("/api/popular-products")
def get_popular_products():
    """인기상품 전용 API"""
    try:
        # 인기 키워드 리스트 (계절별, 트렌드별)
        seasonal_keywords = {
            "가전제품": ["로봇청소기", "에어프라이어", "공기청정기", "커피머신", "전자레인지"],
            "생활용품": ["청소기", "선풍기", "가습기", "제습기", "온풍기"],
            "주방용품": ["전기밥솥", "믹서기", "블렌더", "토스터", "전기포트"],
            "패션": ["여름옷", "가을옷", "운동화", "가방", "모자"],
            "뷰티": ["화장품", "스킨케어", "헤어케어", "향수", "메이크업"]
        }
        
        all_products = []
        
        for category, keywords in seasonal_keywords.items():
            category_products = []
            
            for keyword in keywords:
                try:
                    result = naver_search_api.search_shopping(keyword, 4)  # 각 키워드당 4개
                    if 'items' in result and result['items']:
                        for item in result['items']:
                            product = {
                                "rank": len(all_products) + 1,
                                "product_name": item.get('title', '').replace('<b>', '').replace('</b>', ''),
                                "price": item.get('lprice', '가격 정보 없음'),
                                "product_url": item.get('link', ''),
                                "image_url": item.get('image', ''),
                                "mall_name": item.get('mallName', ''),
                                "category": category,
                                "keyword": keyword
                            }
                            category_products.append(product)
                            all_products.append(product)
                            
                            if len(all_products) >= 50:
                                break
                
                except Exception as e:
                    print(f"키워드 '{keyword}' 검색 중 오류: {e}")
                    continue
                
                if len(all_products) >= 50:
                    break
            
            if len(all_products) >= 50:
                break
        
        return {"items": all_products, "count": len(all_products), "categories": list(seasonal_keywords.keys())}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인기상품 조회 실패: {str(e)}")

@app.get("/api/products/category/{category}")
def get_products_by_category(category: str):
    """카테고리별 상품 조회 API"""
    try:
        # 카테고리별 키워드 매핑
        category_keywords = {
            "가전제품": ["로봇청소기", "에어프라이어", "공기청정기", "커피머신", "전자레인지"],
            "생활용품": ["청소기", "선풍기", "가습기", "제습기", "온풍기"],
            "주방용품": ["전기밥솥", "믹서기", "블렌더", "토스터", "전기포트"],
            "패션": ["여름옷", "가을옷", "운동화", "가방", "모자"],
            "뷰티": ["화장품", "스킨케어", "헤어케어", "향수", "메이크업"]
        }
        
        if category not in category_keywords:
            raise HTTPException(status_code=400, detail="지원하지 않는 카테고리입니다")
        
        keywords = category_keywords[category]
        products = []
        
        for keyword in keywords:
            try:
                result = naver_search_api.search_shopping(keyword, 8)  # 각 키워드당 8개
                if 'items' in result and result['items']:
                    for item in result['items']:
                        product = {
                            "rank": len(products) + 1,
                            "product_name": item.get('title', '').replace('<b>', '').replace('</b>', ''),
                            "price": item.get('lprice', '가격 정보 없음'),
                            "product_url": item.get('link', ''),
                            "image_url": item.get('image', ''),
                            "mall_name": item.get('mallName', ''),
                            "category": category,
                            "keyword": keyword
                        }
                        products.append(product)
                        
                        if len(products) >= 40:  # 카테고리당 최대 40개
                            break
                
                if len(products) >= 40:
                    break
                    
            except Exception as e:
                print(f"키워드 '{keyword}' 검색 중 오류: {e}")
                continue
        
        return {"items": products, "count": len(products), "category": category}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리별 상품 조회 실패: {str(e)}")
