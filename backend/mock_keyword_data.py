#!/usr/bin/env python3
"""
네이버 키워드 API Mock 데이터
"""

import random
from typing import Dict, List, Any

def get_mock_keyword_data(keyword: str) -> Dict[str, Any]:
    """
    키워드에 대한 목업 데이터 생성
    
    Args:
        keyword (str): 키워드
        
    Returns:
        Dict[str, Any]: 키워드 분석 목업 데이터
    """
    
    # 키워드별 특화된 목업 데이터
    keyword_specific_data = {
        "로봇청소기": {
            "avg_competition": 85,
            "related_keywords": [
                "다이슨청소기", "아이로봇", "코봇청소기", "스마트청소기", 
                "무선청소기", "로봇청소기추천", "청소로봇", "자동청소기"
            ],
            "monthly_searches": 45000,
            "trend_direction": "상승"
        },
        "여름원피스": {
            "avg_competition": 70,
            "related_keywords": [
                "미니원피스", "맥시원피스", "플로럴원피스", "여름패션",
                "여름코디", "원피스추천", "여름옷", "여름스타일"
            ],
            "monthly_searches": 32000,
            "trend_direction": "상승"
        },
        "스마트폰": {
            "avg_competition": 95,
            "related_keywords": [
                "갤럭시", "아이폰", "5G폰", "플래그십폰",
                "스마트폰추천", "휴대폰", "모바일", "안드로이드폰"
            ],
            "monthly_searches": 125000,
            "trend_direction": "안정"
        },
        "노트북": {
            "avg_competition": 88,
            "related_keywords": [
                "게이밍노트북", "맥북", "삼성노트북", "LG그램",
                "노트북추천", "랩탑", "휴대용컴퓨터", "노트북브랜드"
            ],
            "monthly_searches": 78000,
            "trend_direction": "상승"
        }
    }
    
    # 키워드에 맞는 특화 데이터 찾기
    specific_data = None
    for key, data in keyword_specific_data.items():
        if key in keyword or keyword in key:
            specific_data = data
            break
    
    # 기본값 설정
    if specific_data:
        base_competition = specific_data["avg_competition"]
        related_keywords = specific_data["related_keywords"]
        monthly_searches = specific_data["monthly_searches"]
        trend_direction = specific_data["trend_direction"]
    else:
        base_competition = random.randint(40, 90)
        related_keywords = [
            f"{keyword}추천", f"{keyword}비교", f"{keyword}브랜드",
            f"{keyword}가격", f"{keyword}후기", f"{keyword}구매"
        ]
        monthly_searches = random.randint(5000, 50000)
        trend_direction = random.choice(["상승", "하락", "안정"])
    
    # 목업 데이터 생성
    mock_data = {
        "keyword": keyword,
        "competition": base_competition,
        "competition_level": "높음" if base_competition > 80 else "보통" if base_competition > 50 else "낮음",
        "monthly_searches": monthly_searches,
        "related_keywords": [
            {
                "keyword": kw,
                "relevance": max(60, 95 - (i * 5)),
                "search_volume": f"{random.randint(1000, 15000):,}",
                "competition": "높음" if i < 3 else "보통"
            }
            for i, kw in enumerate(related_keywords[:8])
        ],
        "search_volume_stats": {
            "daily_searches": monthly_searches // 30,
            "weekly_searches": monthly_searches // 4,
            "monthly_searches": monthly_searches,
            "volume_level": "높음" if monthly_searches > 50000 else "보통" if monthly_searches > 20000 else "낮음",
            "competition": "높음" if base_competition > 80 else "보통",
            "trend_direction": trend_direction,
            "growth_rate": f"{random.randint(5, 25)}%",
            "seasonality": "연중"
        },
        "trend_analysis": {
            "avg_trend": random.randint(40, 90),
            "trend_direction": trend_direction,
            "trend_score": random.randint(60, 95),
            "max_trend": random.randint(80, 100),
            "data_points": 7
        },
        "analysis_insights": [
            f"'{keyword}' 키워드는 {trend_direction} 트렌드를 보이고 있습니다.",
            f"월간 검색량이 {monthly_searches:,}회로 {'높은' if monthly_searches > 50000 else '보통' if monthly_searches > 20000 else '낮은'} 수준입니다.",
            f"경쟁도가 {base_competition}점으로 {'치열한' if base_competition > 80 else '보통' if base_competition > 50 else '낮은'} 경쟁 상황입니다."
        ]
    }
    
    return mock_data

def get_mock_api_response() -> Dict[str, Any]:
    """
    네이버 키워드 API 응답 형태의 목업 데이터
    
    Returns:
        Dict[str, Any]: API 응답 형태 목업 데이터
    """
    return {
        "status": "success",
        "message": "Mock API 응답입니다.",
        "data": {
            "keywords": [
                {
                    "keyword": "테스트키워드",
                    "competition": 75,
                    "monthly_searches": 25000
                }
            ]
        }
    }

def get_mock_keyword_ideas(keyword: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    키워드 아이디어 목업 데이터
    
    Args:
        keyword (str): 기본 키워드
        count (int): 생성할 아이디어 개수
        
    Returns:
        List[Dict[str, Any]]: 키워드 아이디어 목업 데이터
    """
    suffixes = ["추천", "비교", "후기", "가격", "브랜드", "구매", "할인", "이벤트", "신제품", "베스트"]
    prefixes = ["최신", "인기", "신상", "프리미엄", "고급", "저렴한", "할인", "특가"]
    
    ideas = []
    
    # 접미사가 붙은 키워드들
    for suffix in suffixes[:count//2]:
        ideas.append({
            "keyword": f"{keyword}{suffix}",
            "relevance": random.randint(70, 95),
            "search_volume": random.randint(1000, 20000),
            "competition": random.randint(40, 90),
            "competition_level": random.choice(["높음", "보통", "낮음"])
        })
    
    # 접두사가 붙은 키워드들
    for prefix in prefixes[:count//2]:
        ideas.append({
            "keyword": f"{prefix}{keyword}",
            "relevance": random.randint(60, 85),
            "search_volume": random.randint(500, 15000),
            "competition": random.randint(30, 80),
            "competition_level": random.choice(["높음", "보통", "낮음"])
        })
    
    return ideas[:count]

def get_mock_shopping_keywords(keyword: str) -> List[Dict[str, Any]]:
    """
    쇼핑 특화 연관 키워드 목업 데이터
    
    Args:
        keyword (str): 기본 키워드
        
    Returns:
        List[Dict[str, Any]]: 쇼핑 특화 연관 키워드 목업 데이터
    """
    
    # 쇼핑 특화 키워드 데이터
    shopping_keywords = {
        "로봇청소기": [
            {"keyword": "다이슨청소기", "price_range": "50만원 이상", "intent": "브랜드 탐색", "category": "가전"},
            {"keyword": "아이로봇룸바", "price_range": "20만원대", "intent": "브랜드 탐색", "category": "가전"},
            {"keyword": "로봇청소기추천", "price_range": "10만원대", "intent": "구매", "category": "가전"},
            {"keyword": "무선청소기비교", "price_range": "5만원대", "intent": "비교", "category": "가전"},
            {"keyword": "청소기가격비교", "price_range": "다양", "intent": "가격비교", "category": "가전"},
            {"keyword": "스마트청소기할인", "price_range": "할인가", "intent": "할인", "category": "가전"},
            {"keyword": "청소로봇브랜드", "price_range": "다양", "intent": "브랜드 탐색", "category": "가전"},
            {"keyword": "IoT청소기", "price_range": "30만원대", "intent": "기술", "category": "가전"}
        ],
        "여름원피스": [
            {"keyword": "미니원피스", "price_range": "3만원대", "intent": "구매", "category": "패션"},
            {"keyword": "맥시원피스", "price_range": "5만원대", "intent": "구매", "category": "패션"},
            {"keyword": "플로럴원피스", "price_range": "4만원대", "intent": "스타일", "category": "패션"},
            {"keyword": "여름원피스세일", "price_range": "할인가", "intent": "할인", "category": "패션"},
            {"keyword": "원피스브랜드", "price_range": "다양", "intent": "브랜드 탐색", "category": "패션"},
            {"keyword": "여름코디", "price_range": "2만원대", "intent": "코디", "category": "패션"},
            {"keyword": "여름패션", "price_range": "다양", "intent": "트렌드", "category": "패션"},
            {"keyword": "데일리원피스", "price_range": "3만원대", "intent": "구매", "category": "패션"}
        ],
        "스마트폰": [
            {"keyword": "갤럭시S24", "price_range": "100만원대", "intent": "브랜드 탐색", "category": "전자기기"},
            {"keyword": "아이폰15", "price_range": "130만원대", "intent": "브랜드 탐색", "category": "전자기기"},
            {"keyword": "5G스마트폰", "price_range": "80만원대", "intent": "기술", "category": "전자기기"},
            {"keyword": "스마트폰가격비교", "price_range": "다양", "intent": "가격비교", "category": "전자기기"},
            {"keyword": "플래그십폰", "price_range": "100만원 이상", "intent": "프리미엄", "category": "전자기기"},
            {"keyword": "중고폰", "price_range": "30만원대", "intent": "저가", "category": "전자기기"},
            {"keyword": "휴대폰할인", "price_range": "할인가", "intent": "할인", "category": "전자기기"},
            {"keyword": "스마트폰추천", "price_range": "다양", "intent": "구매", "category": "전자기기"}
        ],
        "노트북": [
            {"keyword": "게이밍노트북", "price_range": "150만원대", "intent": "전문용도", "category": "컴퓨터"},
            {"keyword": "맥북프로", "price_range": "200만원 이상", "intent": "브랜드 탐색", "category": "컴퓨터"},
            {"keyword": "삼성노트북", "price_range": "80만원대", "intent": "브랜드 탐색", "category": "컴퓨터"},
            {"keyword": "LG그램", "price_range": "120만원대", "intent": "브랜드 탐색", "category": "컴퓨터"},
            {"keyword": "노트북할인", "price_range": "할인가", "intent": "할인", "category": "컴퓨터"},
            {"keyword": "학생용노트북", "price_range": "50만원대", "intent": "용도별", "category": "컴퓨터"},
            {"keyword": "사무용노트북", "price_range": "60만원대", "intent": "용도별", "category": "컴퓨터"},
            {"keyword": "노트북가격비교", "price_range": "다양", "intent": "가격비교", "category": "컴퓨터"}
        ]
    }
    
    # 키워드에 맞는 쇼핑 특화 데이터 찾기
    shopping_data = []
    for pattern, data_list in shopping_keywords.items():
        if pattern in keyword or keyword in pattern:
            shopping_data = data_list
            break
    
    # 기본 쇼핑 키워드 생성
    if not shopping_data:
        shopping_data = [
            {"keyword": f"{keyword}추천", "price_range": "다양", "intent": "구매", "category": "기타"},
            {"keyword": f"{keyword}가격비교", "price_range": "다양", "intent": "가격비교", "category": "기타"},
            {"keyword": f"{keyword}브랜드", "price_range": "다양", "intent": "브랜드 탐색", "category": "기타"},
            {"keyword": f"{keyword}할인", "price_range": "할인가", "intent": "할인", "category": "기타"},
            {"keyword": f"{keyword}세일", "price_range": "할인가", "intent": "할인", "category": "기타"},
            {"keyword": f"{keyword}후기", "price_range": "다양", "intent": "정보", "category": "기타"}
        ]
    
    # 목업 데이터 생성
    result = []
    for i, item in enumerate(shopping_data):
        result.append({
            "keyword": item["keyword"],
            "relevance": max(70, 95 - (i * 3)),
            "search_volume": f"{random.randint(2000, 25000):,}",
            "competition": random.choice(["높음", "보통", "낮음"]),
            "price_range": item["price_range"],
            "category": item["category"],
            "shopping_score": max(60, 90 - (i * 4)),
            "intent": item["intent"]
        })
    
    return result

def get_mock_shopping_product_data(keyword: str) -> Dict[str, Any]:
    """
    쇼핑 상품 목업 데이터
    
    Args:
        keyword (str): 검색 키워드
        
    Returns:
        Dict[str, Any]: 쇼핑 상품 목업 데이터
    """
    
    # 키워드별 특화 상품 데이터
    product_data = {
        "로봇청소기": {
            "products": [
                {"title": "다이슨 V15 무선청소기", "price": "890000", "brand": "다이슨", "category": "청소기"},
                {"title": "아이로봇 룸바 i7+", "price": "1200000", "brand": "아이로봇", "category": "로봇청소기"},
                {"title": "샤오미 로봇청소기", "price": "180000", "brand": "샤오미", "category": "로봇청소기"},
                {"title": "LG 코드제로 A9", "price": "350000", "brand": "LG", "category": "무선청소기"}
            ]
        },
        "여름원피스": {
            "products": [
                {"title": "플로럴 미니원피스", "price": "35000", "brand": "자라", "category": "원피스"},
                {"title": "린넨 맥시원피스", "price": "48000", "brand": "유니클로", "category": "원피스"},
                {"title": "체크 셔츠원피스", "price": "42000", "brand": "에잇세컨즈", "category": "원피스"},
                {"title": "데님 원피스", "price": "39000", "brand": "스파오", "category": "원피스"}
            ]
        },
        "스마트폰": {
            "products": [
                {"title": "갤럭시 S24 Ultra", "price": "1398000", "brand": "삼성", "category": "스마트폰"},
                {"title": "아이폰 15 Pro", "price": "1550000", "brand": "애플", "category": "스마트폰"},
                {"title": "갤럭시 A54", "price": "449000", "brand": "삼성", "category": "스마트폰"},
                {"title": "아이폰 14", "price": "1250000", "brand": "애플", "category": "스마트폰"}
            ]
        }
    }
    
    # 키워드에 맞는 상품 데이터 찾기
    products = []
    for pattern, data in product_data.items():
        if pattern in keyword or keyword in pattern:
            products = data["products"]
            break
    
    # 기본 상품 데이터
    if not products:
        products = [
            {"title": f"{keyword} 상품 1", "price": "50000", "brand": "브랜드A", "category": "기타"},
            {"title": f"{keyword} 상품 2", "price": "75000", "brand": "브랜드B", "category": "기타"},
            {"title": f"{keyword} 상품 3", "price": "100000", "brand": "브랜드C", "category": "기타"}
        ]
    
    return {
        "total": len(products) * 100,  # 실제로는 더 많은 상품이 있다고 가정
        "display": len(products),
        "keyword": keyword,
        "items": [
            {
                "title": product["title"],
                "link": f"https://shopping.naver.com/search?query={product['title']}",
                "image": "https://via.placeholder.com/200x200",
                "lprice": product["price"],
                "hprice": str(int(product["price"]) + 50000),
                "mallName": "네이버쇼핑",
                "productId": f"{random.randint(1000000, 9999999)}",
                "productType": "1",
                "brand": product["brand"],
                "maker": product["brand"],
                "category1": product["category"],
                "category2": "",
                "category3": "",
                "category4": ""
            }
            for product in products
        ]
    } 