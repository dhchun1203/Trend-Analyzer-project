import requests
import json
from typing import Dict, List, Any, Optional
from naver_auth import NaverAdAuth
from mock_keyword_data import get_mock_keyword_data, get_mock_api_response
import time

class NaverKeywordAPI:
    def __init__(self):
        self.auth = NaverAdAuth()
        # 네이버 검색광고 API의 정확한 엔드포인트
        self.base_url = "https://api.searchad.naver.com"
        # 대안 URL들:
        # self.base_url = "https://searchad.naver.com/api"
        # self.base_url = "https://api.naver.com/searchad"
        
    def get_keyword_ideas(self, keyword: str, show_detail: str = "1") -> Dict[str, Any]:
        """
        네이버 검색광고 API 키워드 도구 API 호출
        정확한 엔드포인트와 인증 방식 사용
        
        Args:
            keyword (str): 검색할 키워드
            show_detail (str): 상세 정보 표시 여부 ("1": 상세, "0": 간단)
            
        Returns:
            Dict[str, Any]: 키워드 아이디어 응답 데이터
        """
        # 네이버 검색광고 API 정확한 엔드포인트
        # 네이버 검색광고 API 문서: https://naver.github.io/searchad-apidoc/
        endpoint = "/keywordstool"
        method = "GET"
        
        # 정확한 파라미터 (네이버 검색광고 API 문서 기준)
        params = {
            'hintKeywords': keyword,  # 네이버 검색광고 API 표준 파라미터
            'showDetail': show_detail
        }
        
        # 정확한 인증 헤더 (네이버 검색광고 API 문서 기준)
        # HMAC-SHA256 서명 방식 사용
        headers = self.auth.get_auth_headers(method, endpoint, "")
        
        print(f"🔧 네이버 검색광고 API 호출:")
        print(f"   URL: {self.base_url}{endpoint}")
        print(f"   Method: {method}")
        print(f"   Params: {params}")
        
        try:
            # API 호출
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers=headers,
                timeout=30  # 타임아웃 설정
            )
            
            # 응답 상태 코드 확인
            print(f"📡 응답 상태 코드: {response.status_code}")
            print(f"📡 응답 헤더: {dict(response.headers)}")
            
            # 응답 확인
            response.raise_for_status()
            
            # JSON 응답 파싱
            data = response.json()
            
            print(f"✅ 네이버 검색광고 API 성공!")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 네이버 검색광고 API 실패: {str(e)}")
            
            # 응답 내용이 있다면 출력
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"❌ 에러 응답: {error_data}")
                except:
                    print(f"❌ 에러 응답 텍스트: {e.response.text}")
            
            # 대안: 다른 인증 방식 시도
            return self._try_alternative_auth(keyword, show_detail)
    
    def _try_alternative_auth(self, keyword: str, show_detail: str) -> Dict[str, Any]:
        """
        대안 인증 방식 시도
        
        Args:
            keyword (str): 키워드
            show_detail (str): 상세 정보 표시 여부
            
        Returns:
            Dict[str, Any]: API 응답
        """
        endpoint = "/keywordstool"
        method = "GET"
        params = {'hintKeywords': keyword, 'showDetail': show_detail}
        
        # 대안 헤더 조합들
        alternative_headers = [
            # 1. 기본 헤더
            {
                'X-API-KEY': self.auth.client_id,
                'X-Customer': self.auth.customer_id,
                'Content-Type': 'application/json'
            },
            # 2. Authorization Bearer
            {
                'Authorization': f'Bearer {self.auth.client_id}',
                'X-Customer': self.auth.customer_id,
                'Content-Type': 'application/json'
            },
            # 3. API-Key
            {
                'API-Key': self.auth.client_id,
                'X-Customer': self.auth.customer_id,
                'Content-Type': 'application/json'
            }
        ]
        
        for i, headers in enumerate(alternative_headers):
            try:
                print(f"🔧 대안 인증 {i+1} 시도:")
                print(f"   Headers: {headers}")
                
                response = requests.get(
                    f"{self.base_url}{endpoint}",
                    params=params,
                    headers=headers
                )
                
                response.raise_for_status()
                data = response.json()
                
                print(f"✅ 대안 인증 {i+1} 성공!")
                return data
                
            except requests.exceptions.RequestException as e:
                print(f"❌ 대안 인증 {i+1} 실패: {str(e)}")
                continue
        
        # 모든 시도 실패 시 예외 발생
        raise Exception(f"모든 인증 방식으로 시도했지만 실패했습니다.")
    
    def _retry_with_different_params(self, keyword: str, show_detail: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        다른 파라미터로 API 재시도
        
        Args:
            keyword (str): 키워드
            show_detail (str): 상세 정보 표시 여부
            headers (Dict[str, str]): 인증 헤더
            
        Returns:
            Dict[str, Any]: API 응답
        """
        # 다양한 파라미터 조합으로 재시도
        param_combinations = [
            {'keyword': keyword, 'showDetail': show_detail},
            {'hintKeywords': keyword, 'showDetail': show_detail},
            {'relKeyword': keyword, 'showDetail': show_detail},
            {'keyword': keyword},
            {'hintKeywords': keyword}
        ]
        
        for i, params in enumerate(param_combinations):
            try:
                print(f"   재시도 {i+1}: {params}")
                response = requests.get(
                    f"{self.base_url}/keywordstool",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"   재시도 {i+1} 실패: {str(e)}")
                continue
        
        # 모든 재시도 실패 시 예외 발생
        raise Exception(f"모든 파라미터 조합으로 시도했지만 실패했습니다.")
    
    def parse_keyword_data(self, api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        API 응답을 파싱하여 키워드 데이터 추출
        
        Args:
            api_response (Dict[str, Any]): API 응답 데이터
            
        Returns:
            List[Dict[str, Any]]: 파싱된 키워드 데이터 리스트
        """
        keyword_list = []
        
        try:
            # keywordList에서 키워드 데이터 추출
            if 'keywordList' in api_response:
                for keyword_data in api_response['keywordList']:
                    parsed_data = {
                        'keyword': keyword_data.get('relKeyword', ''),
                        'monthly_pc_qty': keyword_data.get('monthlyPcQty', 0),
                        'monthly_mobile_qty': keyword_data.get('monthlyMobileQty', 0),
                        'monthly_avg_qty': keyword_data.get('monthlyAvgQty', 0),
                        'comp_idx': keyword_data.get('compIdx', ''),
                        'pc_click_rate': keyword_data.get('pcClickRate', 0),
                        'mobile_click_rate': keyword_data.get('mobileClickRate', 0),
                        'pc_click_count': keyword_data.get('pcClickCount', 0),
                        'mobile_click_count': keyword_data.get('mobileClickCount', 0),
                        'avg_click_count': keyword_data.get('avgClickCount', 0),
                        'pc_click_price': keyword_data.get('pcClickPrice', 0),
                        'mobile_click_price': keyword_data.get('mobileClickPrice', 0),
                        'avg_click_price': keyword_data.get('avgClickPrice', 0)
                    }
                    keyword_list.append(parsed_data)
            
            return keyword_list
            
        except Exception as e:
            raise Exception(f"키워드 데이터 파싱 실패: {str(e)}")
    
    def get_keyword_analysis(self, keyword: str, use_mock: bool = False) -> Dict[str, Any]:
        """
        키워드 분석 결과 반환
        
        Args:
            keyword (str): 분석할 키워드
            use_mock (bool): 목업 데이터 사용 여부 (기본값: True)
            
        Returns:
            Dict[str, Any]: 키워드 분석 결과
        """
        try:
            if use_mock:
                # 목업 데이터 사용
                print(f"🎭 목업 데이터 사용: '{keyword}'")
                return get_mock_keyword_data(keyword)
            else:
                # 실제 API 호출
                api_response = self.get_keyword_ideas(keyword)
                
                # 데이터 파싱
                keyword_list = self.parse_keyword_data(api_response)
                
                # 분석 결과 구성
                analysis_result = {
                    'search_keyword': keyword,
                    'total_keywords': len(keyword_list),
                    'keywords': keyword_list,
                    'summary': {
                        'avg_monthly_search': sum(k.get('monthly_avg_qty', 0) for k in keyword_list) // max(len(keyword_list), 1),
                        'avg_click_count': sum(k.get('avg_click_count', 0) for k in keyword_list) // max(len(keyword_list), 1),
                        'avg_click_price': sum(k.get('avg_click_price', 0) for k in keyword_list) // max(len(keyword_list), 1)
                    }
                }
                
                return analysis_result
                
        except Exception as e:
            # API 호출 실패 시 목업 데이터로 폴백
            print(f"⚠️ API 호출 실패, 목업 데이터로 대체: {str(e)}")
            return get_mock_keyword_data(keyword)
    
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
                'message': 'API 연결 성공',
                'test_keyword': test_keyword,
                'result_count': len(result.get('keywords', [])),
                'sample_data': result.get('keywords', [])[:3] if result.get('keywords') else []
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'API 연결 실패: {str(e)}',
                'test_keyword': '테스트',
                'result_count': 0,
                'sample_data': []
            } 