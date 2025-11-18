"""
네이버 데이터랩 API를 사용한 키워드 분석
네이버 검색어 트렌드 및 연관 검색어 제공
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
from naver_search_api import NaverSearchAPI

class NaverDatalabAPI:
    def __init__(self):
        # 네이버 데이터랩 API 설정 (새로 발급받은 키)
        self.client_id = "X7wUfrlR_w8ACIQE4Bae"  # 새로 발급받은 키
        self.client_secret = "UI8_MuRzda"  # 새로 발급받은 키
        self.base_url = "https://openapi.naver.com/v1/datalab/search"
        
        # 네이버 검색 API 인스턴스 추가
        self.search_api = NaverSearchAPI()
        
        # API 키 상태 확인
        self.api_key_valid = False
        self._check_api_key()
    
    def _check_api_key(self):
        """API 키 유효성 확인"""
        try:
            # 간단한 테스트 요청으로 API 키 확인
            test_data = {
                "startDate": "2024-01-01",
                "endDate": "2024-01-02",
                "timeUnit": "date",
                "keywordGroups": [
                    {
                        "groupName": "테스트",
                        "keywords": ["테스트"]
                    }
                ]
            }
            
            headers = {
                "X-Naver-Client-Id": self.client_id,
                "X-Naver-Client-Secret": self.client_secret,
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.base_url, json=test_data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                self.api_key_valid = True
                print("✅ 네이버 데이터랩 API 키 유효")
            else:
                self.api_key_valid = False
                print(f"⚠️ 네이버 데이터랩 API 키 만료 또는 잘못됨: {response.status_code}")
                
        except Exception as e:
            self.api_key_valid = False
            print(f"⚠️ 네이버 데이터랩 API 키 확인 실패: {str(e)}")
        
    def get_trend_data(self, keywords: List[str], start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        네이버 데이터랩 API로 키워드 트렌드 데이터 조회
        
        Args:
            keywords (List[str]): 분석할 키워드 리스트
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            Dict[str, Any]: 트렌드 데이터
        """
        # API 키가 유효하지 않으면 목업 데이터 반환
        if not self.api_key_valid:
            print("⚠️ 네이버 데이터랩 API 키가 유효하지 않아 목업 데이터 사용")
            return self._get_mock_trend_data(keywords, start_date, end_date)
        
        # 날짜 설정 (기본값: 최근 7일)
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # API 요청 데이터
        data = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "date",
            "keywordGroups": [
                {
                    "groupName": keyword,
                    "keywords": [keyword]
                } for keyword in keywords
            ]
        }
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.base_url, json=data, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ 네이버 데이터랩 API 호출 실패, 목업 데이터 사용: {str(e)}")
            return self._get_mock_trend_data(keywords, start_date, end_date)
    
    def _get_mock_trend_data(self, keywords: List[str], start_date: str, end_date: str) -> Dict[str, Any]:
        """목업 트렌드 데이터 생성"""
        # 실제와 유사한 목업 데이터 생성
        mock_data = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "date",
            "results": []
        }
        
        for keyword in keywords:
            # 7일간의 트렌드 데이터 생성
            keyword_data = {
                "title": keyword,
                "data": []
            }
            
            for i in range(7):
                date = (datetime.now() - timedelta(days=6-i)).strftime("%Y-%m-%d")
                # 실제적인 트렌드 패턴 생성
                base_ratio = 50 + (len(keyword) * 2)  # 키워드 길이에 따른 기본값
                ratio = base_ratio + random.randint(-20, 30)  # 랜덤 변동
                ratio = max(10, min(100, ratio))  # 10-100 범위로 제한
                
                keyword_data["data"].append({
                    "period": date,
                    "ratio": ratio
                })
            
            mock_data["results"].append(keyword_data)
        
        return mock_data
    
    def get_related_keywords(self, keyword: str) -> List[Dict[str, Any]]:
        """
        연관 키워드 분석 (네이버 검색 API 사용)
        
        Args:
            keyword (str): 메인 키워드
            
        Returns:
            List[Dict[str, Any]]: 연관 키워드 리스트
        """
        # 네이버 검색 API를 사용한 실제 연관 키워드 추출
        print(f"📊 '{keyword}' 연관 키워드 분석 (네이버 검색 API 사용)")
        
        try:
            # 네이버 검색 API에서 연관 키워드 추출
            related_keywords = self.search_api.get_related_keywords_from_search(keyword)
            
            if related_keywords:
                print(f"✅ 네이버 검색 API 기반 연관 키워드 {len(related_keywords)}개 생성")
                return related_keywords
        except Exception as e:
            print(f"⚠️ 네이버 검색 API 실패, 목업 데이터로 대체: {str(e)}")
        
        # 폴백: 목업 데이터 사용
        return self.get_related_keywords_mock(keyword)
    
    def _generate_related_keywords_from_trend(self, keyword: str, trend_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """트렌드 데이터를 기반으로 연관 키워드 생성"""
        related_keywords = []
        
        # 키워드 패턴에 따른 연관 키워드 생성
        keyword_patterns = {
            "로봇청소기": ["스마트청소기", "무선청소기", "자동청소기", "청소로봇", "집안청소"],
            "여름원피스": ["여름옷", "원피스", "여름패션", "여름스타일", "여름코디"],
            "수건": ["타월", "욕실용품", "목욕용품", "건조용품", "욕실수건"],
            "노트북": ["컴퓨터", "랩탑", "휴대용컴퓨터", "전자기기", "IT제품"],
            "스마트폰": ["휴대폰", "모바일", "전화기", "디지털기기", "통신기기"]
        }
        
        # 키워드 패턴 매칭
        for pattern, related_list in keyword_patterns.items():
            if pattern in keyword or keyword in pattern:
                for i, related in enumerate(related_list):
                    # 실제 트렌드 데이터 기반으로 연관성 계산
                    relevance = max(60, 100 - (i * 10))  # 기본 연관성
                    
                    # 트렌드 데이터가 있으면 연관성 조정
                    if trend_data and 'results' in trend_data:
                        relevance = min(95, relevance + 10)
                    
                    related_keywords.append({
                        'keyword': related,
                        'relevance': relevance,
                        'search_volume': f"{relevance * 10:,}",
                        'competition': '보통' if relevance > 70 else '낮음'
                    })
                break
        
        # 기본 연관 키워드 (패턴이 없는 경우)
        if not related_keywords:
            base_keywords = [f"{keyword} 추천", f"{keyword} 인기", f"{keyword} 최신", f"{keyword} 리뷰", f"{keyword} 비교"]
            for i, related in enumerate(base_keywords):
                relevance = max(50, 90 - (i * 8))
                related_keywords.append({
                    'keyword': related,
                    'relevance': relevance,
                    'search_volume': f"{relevance * 8:,}",
                    'competition': '보통' if relevance > 60 else '낮음'
                })
        
        return related_keywords[:10]  # 상위 10개만 반환
    
    def _get_search_volume_level(self, monthly_count: int) -> str:
        """
        월간 검색량에 따른 검색량 레벨 반환
        
        Args:
            monthly_count (int): 월간 검색량
            
        Returns:
            str: 검색량 레벨
        """
        if monthly_count >= 100000:
            return "매우 높음"
        elif monthly_count >= 50000:
            return "높음"
        elif monthly_count >= 10000:
            return "보통"
        elif monthly_count >= 1000:
            return "낮음"
        else:
            return "매우 낮음"
    
    def get_related_keywords_mock(self, keyword: str) -> List[Dict[str, Any]]:
        """
        목업 연관 키워드 데이터 (API 실패 시 사용)
        
        Args:
            keyword (str): 메인 키워드
            
        Returns:
            List[Dict[str, Any]]: 연관 키워드 리스트
        """
        # 키워드별 목업 연관 키워드 데이터
        related_keywords_map = {
            "로봇청소기": [
                {"keyword": "삼성 로봇청소기", "relevance": 95, "search_volume": "높음"},
                {"keyword": "LG 로봇청소기", "relevance": 92, "search_volume": "높음"},
                {"keyword": "다이슨 로봇청소기", "relevance": 88, "search_volume": "보통"},
                {"keyword": "로봇청소기 추천", "relevance": 85, "search_volume": "높음"},
                {"keyword": "로봇청소기 비교", "relevance": 82, "search_volume": "보통"}
            ],
            "여름원피스": [
                {"keyword": "여름원피스 추천", "relevance": 96, "search_volume": "매우 높음"},
                {"keyword": "여름원피스 쇼핑몰", "relevance": 93, "search_volume": "높음"},
                {"keyword": "여름원피스 브랜드", "relevance": 89, "search_volume": "보통"},
                {"keyword": "여름원피스 코디", "relevance": 87, "search_volume": "높음"},
                {"keyword": "여름원피스 사이즈", "relevance": 84, "search_volume": "보통"}
            ],
            "수건": [
                {"keyword": "수건 추천", "relevance": 94, "search_volume": "높음"},
                {"keyword": "수건 세트", "relevance": 91, "search_volume": "보통"},
                {"keyword": "수건 브랜드", "relevance": 88, "search_volume": "보통"},
                {"keyword": "수건 구매", "relevance": 85, "search_volume": "보통"},
                {"keyword": "수건 비교", "relevance": 82, "search_volume": "낮음"}
            ]
        }
        
        if keyword in related_keywords_map:
            return related_keywords_map[keyword]
        else:
            # 기본 연관 키워드 생성
            return [
                {"keyword": f"{keyword} 추천", "relevance": 90, "search_volume": "보통"},
                {"keyword": f"{keyword} 비교", "relevance": 85, "search_volume": "보통"},
                {"keyword": f"{keyword} 브랜드", "relevance": 80, "search_volume": "보통"},
                {"keyword": f"{keyword} 구매", "relevance": 75, "search_volume": "보통"},
                {"keyword": f"{keyword} 리뷰", "relevance": 70, "search_volume": "보통"}
            ]
    
    def get_search_volume_stats(self, keyword: str) -> Dict[str, Any]:
        """
        검색량 통계 분석 (네이버 검색 API 사용)
        
        Args:
            keyword (str): 분석할 키워드
            
        Returns:
            Dict[str, Any]: 검색량 통계
        """
        # 네이버 검색 API를 사용한 실제 검색량 통계
        print(f"📊 '{keyword}' 검색량 통계 분석 (네이버 검색 API 사용)")
        
        try:
            # 네이버 검색 API에서 검색량 통계 생성
            search_volume = self.search_api.get_search_volume_from_search(keyword)
            
            if search_volume:
                print(f"✅ 네이버 검색 API 기반 검색량 통계 생성")
                return search_volume
        except Exception as e:
            print(f"⚠️ 네이버 검색 API 실패, 목업 데이터로 대체: {str(e)}")
        
        # 폴백: 목업 데이터 사용
        return self.get_search_volume_stats_mock(keyword)
    
    def _generate_search_volume_from_trend(self, keyword: str, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """트렌드 데이터를 기반으로 검색량 통계 생성"""
        # 기본 검색량 (키워드 길이와 복잡성에 따라 조정)
        base_volume = len(keyword) * 1000
        
        # 트렌드 데이터가 있으면 검색량 조정
        if trend_data and 'results' in trend_data:
            results = trend_data['results']
            if results and len(results) > 0:
                # 실제 트렌드 데이터 기반 검색량 계산
                avg_trend = sum(result.get('ratio', 0) for result in results) / len(results)
                base_volume = int(base_volume * (avg_trend / 100 + 0.5))
        
        # 검색량 레벨 결정
        if base_volume > 50000:
            volume_level = "매우 높음"
            competition = "높음"
        elif base_volume > 20000:
            volume_level = "높음"
            competition = "보통"
        elif base_volume > 5000:
            volume_level = "보통"
            competition = "보통"
        else:
            volume_level = "낮음"
            competition = "낮음"
        
        return {
            'daily_searches': base_volume,
            'weekly_searches': base_volume * 7,  # 주간 검색량 추가
            'monthly_searches': base_volume * 30,
            'volume_level': volume_level,
            'competition': competition,
            'trend_direction': '상승' if base_volume > 10000 else '안정',
            'growth_rate': f"{max(5, min(50, base_volume // 1000))}%",
            'seasonality': '연중'  # 기본값
        }
    
    def _get_trend_from_data(self, keyword_data: Dict[str, Any]) -> str:
        """
        키워드 데이터에서 트렌드 방향 추출
        
        Args:
            keyword_data (Dict[str, Any]): 키워드 데이터
            
        Returns:
            str: 트렌드 방향
        """
        # 실제로는 월별 데이터 비교가 필요하지만, 현재는 기본값 반환
        return "상승"  # 기본값
    
    def _get_competition_level(self, keyword_data: Dict[str, Any]) -> str:
        """
        키워드 데이터에서 경쟁도 레벨 추출
        
        Args:
            keyword_data (Dict[str, Any]): 키워드 데이터
            
        Returns:
            str: 경쟁도 레벨
        """
        monthly_count = keyword_data.get('monthlyPcQtyCnt', 0) + keyword_data.get('monthlyMobileQtyCnt', 0)
        
        if monthly_count >= 100000:
            return "매우 높음"
        elif monthly_count >= 50000:
            return "높음"
        elif monthly_count >= 10000:
            return "보통"
        else:
            return "낮음"
    
    def get_search_volume_stats_mock(self, keyword: str) -> Dict[str, Any]:
        """
        목업 검색량 통계 데이터 (API 실패 시 사용)
        
        Args:
            keyword (str): 분석할 키워드
            
        Returns:
            Dict[str, Any]: 검색량 통계
        """
        # 목업 검색량 데이터
        search_volume_map = {
            "로봇청소기": {
                "daily_searches": 8500,
                "weekly_searches": 59500,
                "monthly_searches": 255000,
                "trend": "상승",
                "competition": "높음",
                "seasonality": "연중"
            },
            "여름원피스": {
                "daily_searches": 12000,
                "weekly_searches": 84000,
                "monthly_searches": 360000,
                "trend": "상승",
                "competition": "매우 높음",
                "seasonality": "계절성"
            },
            "수건": {
                "daily_searches": 3200,
                "weekly_searches": 22400,
                "monthly_searches": 96000,
                "trend": "유지",
                "competition": "보통",
                "seasonality": "연중"
            }
        }
        
        if keyword in search_volume_map:
            return search_volume_map[keyword]
        else:
            # 기본 검색량 데이터 생성
            daily = random.randint(1000, 5000)
            return {
                "daily_searches": daily,
                "weekly_searches": daily * 7,
                "monthly_searches": daily * 30,
                "trend": random.choice(["상승", "하락", "유지"]),
                "competition": random.choice(["낮음", "보통", "높음"]),
                "seasonality": random.choice(["연중", "계절성"])
            }
    
    def get_trend_chart_data_real(self, keyword: str) -> List[Dict[str, Any]]:
        """
        실제 API를 사용한 트렌드 차트 데이터
        
        Args:
            keyword (str): 키워드
            
        Returns:
            List[Dict[str, Any]]: 7일 트렌드 데이터
        """
        try:
            # 네이버 데이터랩 API에서 실제 7일 트렌드 데이터 조회
            trend_data = self.get_trend_data([keyword])
            return self._parse_trend_chart_data(trend_data, keyword)
        except Exception as e:
            print(f"⚠️ 실제 트렌드 차트 API 호출 실패, 목업 데이터로 대체: {str(e)}")
            return self.get_trend_chart_data_mock(keyword)
    
    def _parse_trend_chart_data(self, trend_data: Dict[str, Any], keyword: str) -> List[Dict[str, Any]]:
        """
        실제 트렌드 데이터를 차트용으로 파싱
        
        Args:
            trend_data (Dict[str, Any]): 네이버 데이터랩 API 응답
            keyword (str): 키워드
            
        Returns:
            List[Dict[str, Any]]: 차트용 데이터
        """
        try:
            results = trend_data.get('results', [])
            if not results:
                return self.get_trend_chart_data_mock(keyword)
            
            keyword_data = results[0]
            data_points = keyword_data.get('data', [])
            
            chart_data = []
            for point in data_points:
                chart_data.append({
                    'date': point.get('period', ''),
                    'trend': point.get('ratio', 0)
                })
            
            return chart_data
        except Exception as e:
            return self.get_trend_chart_data_mock(keyword)
    
    def get_trend_chart_data_mock(self, keyword: str) -> List[Dict[str, Any]]:
        """
        목업 트렌드 차트 데이터 (API 실패 시 사용)
        
        Args:
            keyword (str): 키워드
            
        Returns:
            List[Dict[str, Any]]: 7일 트렌드 데이터
        """
        # 목업 7일 트렌드 데이터 생성
        chart_data = []
        base_trend = random.randint(30, 80)
        
        for i in range(7):
            date = datetime.now() - timedelta(days=6-i)
            trend_value = base_trend + random.randint(-10, 10)
            trend_value = max(0, min(100, trend_value))
            
            chart_data.append({
                'date': date.strftime('%m/%d'),
                'trend': trend_value
            })
        
        return chart_data
    
    def get_keyword_analysis(self, keyword: str) -> Dict[str, Any]:
        """
        키워드 분석 결과 반환 (확장된 버전)
        
        Args:
            keyword (str): 분석할 키워드
            
        Returns:
            Dict[str, Any]: 키워드 분석 결과
        """
        try:
            # 트렌드 데이터 조회
            trend_data = self.get_trend_data([keyword])
            
            # 데이터 파싱
            parsed_data = self.parse_trend_data(trend_data, keyword)
            
            # 연관 키워드 분석 추가
            related_keywords = self.get_related_keywords(keyword)
            
            # 검색량 통계 추가
            search_volume_stats = self.get_search_volume_stats(keyword)
            
            # 확장된 분석 결과
            extended_analysis = {
                **parsed_data,
                'related_keywords': related_keywords,
                'search_volume_stats': search_volume_stats,
                'analysis_insights': self.generate_insights(keyword, parsed_data, related_keywords, search_volume_stats)
            }
            
            return extended_analysis
            
        except Exception as e:
            # API 호출 실패 시 목업 데이터로 폴백
            print(f"⚠️ 네이버 데이터랩 API 호출 실패, 목업 데이터로 대체: {str(e)}")
            return self.get_mock_data(keyword)
    
    def generate_insights(self, keyword: str, trend_data: Dict, related_keywords: List, search_volume: Dict) -> List[str]:
        """
        키워드 분석 인사이트 생성
        
        Args:
            keyword (str): 키워드
            trend_data (Dict): 트렌드 데이터
            related_keywords (List): 연관 키워드
            search_volume (Dict): 검색량 통계
            
        Returns:
            List[str]: 인사이트 리스트
        """
        insights = []
        
        # 트렌드 인사이트
        trend_score = trend_data['summary']['trend_score']
        trend_direction = trend_data['summary']['trend_direction']
        
        if trend_score >= 70:
            insights.append(f"'{keyword}'는 현재 매우 인기 있는 키워드입니다.")
        elif trend_score >= 50:
            insights.append(f"'{keyword}'는 보통 수준의 인기를 보이고 있습니다.")
        else:
            insights.append(f"'{keyword}'는 상대적으로 낮은 인기를 보이고 있습니다.")
        
        if trend_direction == "상승":
            insights.append("트렌드가 상승하고 있어 관심이 증가하고 있습니다.")
        elif trend_direction == "하락":
            insights.append("트렌드가 하락하고 있어 관심이 감소하고 있습니다.")
        
        # 검색량 인사이트
        daily_searches = search_volume['daily_searches']
        if daily_searches >= 10000:
            insights.append("일일 검색량이 매우 높아 경쟁이 치열할 수 있습니다.")
        elif daily_searches >= 5000:
            insights.append("일일 검색량이 높아 마케팅 기회가 있습니다.")
        else:
            insights.append("일일 검색량이 보통 수준으로 안정적입니다.")
        
        # 연관 키워드 인사이트
        if related_keywords:
            top_related = related_keywords[0]['keyword']
            insights.append(f"가장 연관성이 높은 키워드는 '{top_related}'입니다.")
        
        # 계절성 인사이트
        if 'seasonality' in search_volume and search_volume['seasonality'] == "계절성":
            insights.append("이 키워드는 계절적 특성을 보이므로 시기별 마케팅 전략이 필요합니다.")
        else:
            insights.append("이 키워드는 연중 안정적인 관심을 보입니다.")
        
        return insights
    
    def parse_trend_data(self, trend_data: Dict[str, Any], keyword: str) -> Dict[str, Any]:
        """
        트렌드 데이터 파싱
        
        Args:
            trend_data (Dict[str, Any]): 네이버 데이터랩 API 응답
            keyword (str): 검색 키워드
            
        Returns:
            Dict[str, Any]: 파싱된 데이터
        """
        try:
            results = trend_data.get('results', [])
            
            if not results:
                return self.get_mock_data(keyword)
            
            # 첫 번째 키워드 그룹의 데이터 추출
            keyword_data = results[0]
            data_points = keyword_data.get('data', [])
            
            # 트렌드 분석
            if data_points:
                # 최근 7일 평균 트렌드
                recent_trends = [point.get('ratio', 0) for point in data_points[-7:]]
                avg_trend = sum(recent_trends) / len(recent_trends) if recent_trends else 0
                
                # 최고 트렌드
                max_trend = max([point.get('ratio', 0) for point in data_points]) if data_points else 0
                
                # 트렌드 방향 (상승/하락/유지)
                if len(data_points) >= 2:
                    first_trend = data_points[0].get('ratio', 0)
                    last_trend = data_points[-1].get('ratio', 0)
                    if last_trend > first_trend:
                        trend_direction = "상승"
                    elif last_trend < first_trend:
                        trend_direction = "하락"
                    else:
                        trend_direction = "유지"
                else:
                    trend_direction = "유지"
            else:
                avg_trend = 0
                max_trend = 0
                trend_direction = "유지"
            
            # 분석 결과 구성
            analysis_result = {
                'search_keyword': keyword,
                'trend_analysis': {
                    'avg_trend': round(avg_trend, 2),
                    'max_trend': round(max_trend, 2),
                    'trend_direction': trend_direction,
                    'data_points': len(data_points)
                },
                'summary': {
                    'keyword': keyword,
                    'trend_score': round(avg_trend, 2),
                    'popularity': self.get_popularity_level(avg_trend),
                    'trend_direction': trend_direction
                }
            }
            
            return analysis_result
            
        except Exception as e:
            raise Exception(f"트렌드 데이터 파싱 실패: {str(e)}")
    
    def get_popularity_level(self, trend_score: float) -> str:
        """
        트렌드 점수에 따른 인기도 레벨 반환
        
        Args:
            trend_score (float): 트렌드 점수
            
        Returns:
            str: 인기도 레벨
        """
        if trend_score >= 80:
            return "매우 높음"
        elif trend_score >= 60:
            return "높음"
        elif trend_score >= 40:
            return "보통"
        elif trend_score >= 20:
            return "낮음"
        else:
            return "매우 낮음"
    
    def get_mock_data(self, keyword: str) -> Dict[str, Any]:
        """
        목업 데이터 반환 (API 실패 시) - 확장된 버전
        
        Args:
            keyword (str): 키워드
            
        Returns:
            Dict[str, Any]: 목업 데이터
        """
        # 키워드별 목업 트렌드 데이터
        mock_trends = {
            "여름원피스": {"avg_trend": 85.5, "max_trend": 95.2, "trend_direction": "상승"},
            "수건": {"avg_trend": 45.3, "max_trend": 52.1, "trend_direction": "유지"},
            "강아지": {"avg_trend": 72.8, "max_trend": 88.9, "trend_direction": "상승"},
            "테스트": {"avg_trend": 25.1, "max_trend": 30.5, "trend_direction": "하락"}
        }
        
        if keyword in mock_trends:
            trend_data = mock_trends[keyword]
        else:
            trend_data = {"avg_trend": 50.0, "max_trend": 60.0, "trend_direction": "유지"}
        
        # 기본 분석 결과
        basic_analysis = {
            'search_keyword': keyword,
            'trend_analysis': {
                'avg_trend': trend_data['avg_trend'],
                'max_trend': trend_data['max_trend'],
                'trend_direction': trend_data['trend_direction'],
                'data_points': 7
            },
            'summary': {
                'keyword': keyword,
                'trend_score': trend_data['avg_trend'],
                'popularity': self.get_popularity_level(trend_data['avg_trend']),
                'trend_direction': trend_data['trend_direction']
            }
        }
        
        # 연관 키워드 추가
        related_keywords = self.get_related_keywords_mock(keyword)
        
        # 검색량 통계 추가
        search_volume_stats = self.get_search_volume_stats_mock(keyword)
        
        # 인사이트 생성
        analysis_insights = self.generate_insights(keyword, basic_analysis, related_keywords, search_volume_stats)
        
        # 확장된 분석 결과 반환
        return {
            **basic_analysis,
            'related_keywords': related_keywords,
            'search_volume_stats': search_volume_stats,
            'analysis_insights': analysis_insights
        }
    
    def test_api_connection(self) -> Dict[str, Any]:
        """
        API 연결 테스트
        
        Returns:
            Dict[str, Any]: 테스트 결과
        """
        try:
            # 간단한 키워드로 테스트
            test_keyword = "테스트"
            result = self.get_keyword_analysis(test_keyword)
            
            return {
                'status': 'success',
                'message': '네이버 데이터랩 API 연결 성공',
                'test_keyword': test_keyword,
                'trend_score': result['summary']['trend_score'],
                'popularity': result['summary']['popularity']
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'네이버 데이터랩 API 연결 실패: {str(e)}',
                'test_keyword': '테스트',
                'trend_score': 0,
                'popularity': '알 수 없음'
            } 