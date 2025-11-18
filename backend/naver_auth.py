import requests
import base64
import hashlib
import hmac
import time
import json
import os
from typing import Optional, Dict, Any
from urllib.parse import urlencode

class NaverAdAuth:
    def __init__(self):
        # 네이버 광고 API 인증 정보 (새로 발급받은 키)
        self.client_id = "01000000000852b6f2ba38acb1e395ff70a0196da375c4df743c4cf2c1aca2d716e6733414"
        self.client_secret = "AQAAAAAI1pQwbjadChZ4ooCaFgVjBxGBRR6y1vlSYDhaSe5Lng=="
        self.customer_id = "4094007"
        
        # OAuth 2.0 엔드포인트 (네이버 검색광고 API)
        self.auth_url = "https://searchad.naver.com/login/oauth/authorize.naver"
        self.token_url = "https://searchad.naver.com/oauth/token"
        
        # 리다이렉트 URI (로컬 테스트용)
        self.redirect_uri = "http://localhost:8000/auth/callback"
        
        # Access Token 저장
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        
    def generate_auth_url(self) -> str:
        """Authorization Code를 받기 위한 URL 생성"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self._generate_state(),
            'scope': 'searchad'  # 네이버 검색광고 API 스코프
        }
        
        auth_url = f"{self.auth_url}?{urlencode(params)}"
        return auth_url
    
    def _generate_state(self) -> str:
        """CSRF 방지를 위한 state 값 생성"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def get_access_token_direct(self) -> Dict[str, Any]:
        """네이버 검색광고 API는 별도의 Access Token 없이 API Key 방식 사용"""
        # 네이버 검색광고 API는 Access Token 대신 API Key + Secret Key + Customer ID 사용
        # 실제 API 호출 시 HMAC-SHA256 서명으로 인증
        
        # 가상의 토큰 데이터 (실제로는 API Key를 사용)
        token_data = {
            'access_token': 'NAVER_SEARCHAD_API_KEY',
            'expires_in': 3600,
            'token_type': 'Bearer'
        }
        
        # API Key 정보 저장
        self.access_token = self.client_id  # API Key를 Access Token으로 사용
        self.token_expires_at = time.time() + 3600
        
        return token_data
    
    def exchange_code_for_token(self, authorization_code: str) -> Dict[str, Any]:
        """Authorization Code를 Access Token으로 교환 (일반 OAuth 2.0)"""
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # 토큰 정보 저장
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            self.token_expires_at = time.time() + token_data.get('expires_in', 3600)
            
            return token_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"토큰 발급 실패: {str(e)}")
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh Token을 사용하여 Access Token 갱신"""
        if not self.refresh_token:
            raise Exception("Refresh Token이 없습니다.")
        
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # 새로운 토큰 정보 저장
            self.access_token = token_data.get('access_token')
            if 'refresh_token' in token_data:
                self.refresh_token = token_data.get('refresh_token')
            self.token_expires_at = time.time() + token_data.get('expires_in', 3600)
            
            return token_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"토큰 갱신 실패: {str(e)}")
    
    def is_token_valid(self) -> bool:
        """Access Token이 유효한지 확인"""
        if not self.access_token:
            return False
        
        # 만료 시간 체크 (5분 여유)
        if self.token_expires_at and time.time() > (self.token_expires_at - 300):
            return False
        
        return True
    
    def get_valid_access_token(self) -> str:
        """유효한 Access Token 반환 (필요시 갱신)"""
        if not self.is_token_valid():
            if self.refresh_token:
                self.refresh_access_token()
            else:
                raise Exception("유효한 Access Token이 없습니다. 인증을 다시 진행해주세요.")
        
        return self.access_token
    
    def generate_signature(self, timestamp: str, method: str, uri: str, body: str = "") -> str:
        """HMAC-SHA256 서명 생성 (네이버 검색광고 API 표준)"""
        # 네이버 검색광고 API 서명 생성 방식
        # 메시지 형식: {timestamp}.{method}.{uri}.{body}
        message = f"{timestamp}.{method}.{uri}.{body}"
        
        print(f"🔧 서명 생성 디버깅:")
        print(f"   Timestamp: {timestamp}")
        print(f"   Method: {method}")
        print(f"   URI: {uri}")
        print(f"   Body: '{body}'")
        print(f"   Message: '{message}'")
        print(f"   Secret Key: {self.client_secret[:20]}...")
        
        # HMAC-SHA256 서명 생성
        signature = hmac.new(
            self.client_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Base64 인코딩
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        print(f"   Generated Signature: {signature_b64}")
        
        return signature_b64
    
    def get_auth_headers(self, method: str, uri: str, body: str = "") -> Dict[str, str]:
        """네이버 검색광고 API 요청에 필요한 헤더 생성"""
        # 네이버 검색광고 API는 API Key + Secret Key + Customer ID + HMAC-SHA256 서명 사용
        timestamp = str(int(time.time() * 1000))
        signature = self.generate_signature(timestamp, method, uri, body)
        
        # 네이버 검색광고 API 정확한 헤더 설정
        # 네이버 검색광고 API 문서: https://naver.github.io/searchad-apidoc/
        # 실제 API 문서에 따르면 다음 헤더들이 필요합니다:
        # - X-Timestamp: 요청 시간 (밀리초)
        # - X-API-KEY: API 키
        # - X-Customer: 고객 ID
        # - X-Signature: HMAC-SHA256 서명
        headers = {
            'X-Timestamp': timestamp,
            'X-API-KEY': self.client_id,  # API Key
            'X-Customer': self.customer_id,  # Customer ID
            'X-Signature': signature,  # HMAC-SHA256 서명
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 디버깅을 위한 헤더 출력
        print(f"🔧 네이버 검색광고 API 헤더:")
        print(f"   X-Timestamp: {timestamp}")
        print(f"   X-API-KEY: {self.client_id[:20]}...")
        print(f"   X-Customer: {self.customer_id}")
        print(f"   X-Signature: {signature[:20]}...")
        print(f"   Content-Type: application/json")
        print(f"   Accept: application/json")
        
        return headers
    
    def save_token_to_env(self):
        """토큰을 환경 변수로 저장"""
        if self.access_token:
            os.environ['NAVER_API_ACCESS_TOKEN'] = self.access_token
        if self.refresh_token:
            os.environ['NAVER_API_REFRESH_TOKEN'] = self.refresh_token
        if self.token_expires_at:
            os.environ['NAVER_API_TOKEN_EXPIRES_AT'] = str(self.token_expires_at)
    
    def load_token_from_env(self):
        """환경 변수에서 토큰 로드"""
        self.access_token = os.environ.get('NAVER_API_ACCESS_TOKEN')
        self.refresh_token = os.environ.get('NAVER_API_REFRESH_TOKEN')
        expires_at = os.environ.get('NAVER_API_TOKEN_EXPIRES_AT')
        if expires_at:
            self.token_expires_at = float(expires_at) 