# 네이버 광고 API 인증 가이드

## 🔐 1단계: Access Token 발급

### 📋 사전 준비사항
- ✅ 네이버 광고 계정 생성 완료
- ✅ 애플리케이션 등록 완료
- ✅ Client ID, Client Secret, Customer ID 발급 완료

### 🚀 인증 진행 방법

#### 방법 1: 테스트 스크립트 사용 (권장)

```bash
# 백엔드 디렉토리로 이동
cd backend

# 테스트 스크립트 실행
python test_auth.py
```

1. 메뉴에서 "1. 새로운 인증 진행" 선택
2. **"1. API Key 방식 (권장)"** 선택 (간단한 방법)
3. 또는 **"2. Authorization Code 방식"** 선택 (브라우저 인증 필요)

#### 방법 2: API 엔드포인트 사용

```bash
# API Key 방식으로 직접 인증 설정
curl -X POST http://localhost:8000/auth/token/direct

# 또는 Authorization Code 방식
curl http://localhost:8000/auth/naver
```

#### 방법 3: API 엔드포인트 사용 (Authorization Code 방식)

```bash
# 1. 인증 URL 생성
curl http://localhost:8000/auth/naver

# 2. 브라우저에서 인증 URL 접속 후 권한 승인

# 3. 콜백 URL에서 code 파라미터 추출
# http://localhost:8000/auth/callback?code=YOUR_CODE&state=STATE

# 4. 인증 상태 확인
curl http://localhost:8000/auth/status

# 5. 인증 테스트
curl http://localhost:8000/auth/test
```

### 🔧 API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/auth/token/direct` | POST | API Key 방식 인증 설정 |
| `/auth/naver` | GET | 인증 URL 생성 |
| `/auth/callback` | GET | 인증 콜백 처리 |
| `/auth/status` | GET | 인증 상태 확인 |
| `/auth/refresh` | POST | 토큰 갱신 |
| `/auth/test` | GET | 인증 테스트 |

### 📊 응답 예시

#### 인증 URL 생성
```json
{
  "auth_url": "https://searchad.naver.com/login/oauth/authorize.naver?response_type=code&client_id=...",
  "message": "브라우저에서 위 URL로 접속하여 인증을 완료하세요."
}
```

#### 인증 완료
```json
{
  "message": "인증이 완료되었습니다!",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### 인증 상태 확인
```json
{
  "is_authenticated": true,
  "has_access_token": true,
  "has_refresh_token": true,
  "token_expires_at": 1640995200.0
}
```

### 🔄 토큰 갱신

Access Token은 1시간 후 만료됩니다. 자동 갱신을 위해:

```bash
# 수동 갱신
curl -X POST http://localhost:8000/auth/refresh

# 또는 테스트 스크립트 사용
python test_auth.py
# 메뉴에서 "2. 토큰 갱신 테스트" 선택
```

### 🛠 환경 변수

토큰은 자동으로 환경 변수에 저장됩니다:

- `NAVER_API_ACCESS_TOKEN`: Access Token
- `NAVER_API_REFRESH_TOKEN`: Refresh Token  
- `NAVER_API_TOKEN_EXPIRES_AT`: 만료 시간

### ❗ 주의사항

1. **보안**: 토큰 정보를 안전하게 보관하세요
2. **만료**: Access Token은 1시간 후 만료됩니다
3. **리다이렉트 URI**: 로컬 테스트용으로 `http://localhost:8000/auth/callback` 사용
4. **네트워크**: 인터넷 연결이 필요합니다

### 🐛 문제 해결

#### 인증 실패 시
1. 네이버 광고 계정 상태 확인
2. 애플리케이션 등록 상태 확인
3. Client ID/Secret 정확성 확인
4. 네트워크 연결 상태 확인

#### 토큰 만료 시
1. Refresh Token으로 자동 갱신 시도
2. 갱신 실패 시 재인증 진행

### 📝 다음 단계

✅ Access Token 발급 완료 후 → **2단계: 연관 키워드 조회 API 호출** 진행 