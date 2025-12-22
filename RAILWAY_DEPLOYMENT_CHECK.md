# Railway 배포 확인 가이드

## 🔍 현재 문제점

1. **CORS 오류**: Vercel 도메인에서 Railway API 호출 시 CORS 차단
2. **404 오류**: API 엔드포인트가 제대로 작동하지 않음

## ✅ 해결 방법

### 1. Railway 백엔드 재배포 확인

Railway 대시보드에서:
1. 프로젝트 선택
2. "Deployments" 탭 확인
3. 최신 배포가 완료되었는지 확인
4. 필요시 "Redeploy" 버튼 클릭

### 2. CORS 설정 확인

백엔드 코드에서 CORS 설정이 업데이트되었는지 확인:
- `allow_origin_regex`에 Vercel 도메인 패턴 포함
- 정규식: `r"https://.*\.github\.io|https://.*\.vercel\.app|https://.*-.*\.vercel\.app"`

### 3. API 엔드포인트 테스트

Railway API가 정상 작동하는지 확인:
```bash
# API 엔드포인트 테스트
curl https://trend-analyzer-project-production.up.railway.app/api/popular-products

# 또는 브라우저에서 직접 접속
https://trend-analyzer-project-production.up.railway.app/docs
```

### 4. 네이버 API 키 확인

현재 네이버 API 키는 코드에 하드코딩되어 있습니다:
- **검색 API**: `naver_search_api.py`에 설정됨
- **데이터랩 API**: `naver_datalab_api.py`에 설정됨
- **광고 API**: `naver_auth.py`에 설정됨

**Railway 환경 변수 설정 불필요** (코드에 하드코딩되어 있음)

## 🚨 문제 해결 체크리스트

- [ ] Railway 백엔드가 최신 코드로 재배포되었는지 확인
- [ ] Railway API가 정상 작동하는지 테스트 (`/docs` 접속)
- [ ] CORS 설정이 올바르게 적용되었는지 확인
- [ ] Vercel 도메인이 CORS 정규식에 매칭되는지 확인

## 📝 참고사항

### Vercel 도메인 형식
- Preview: `https://project-name-{hash}-{username}.vercel.app`
- Production: `https://project-name.vercel.app` 또는 커스텀 도메인

### CORS 정규식 설명
```python
r"https://.*\.github\.io|https://.*\.vercel\.app|https://.*-.*\.vercel\.app"
```
- `https://.*\.github\.io`: 모든 GitHub Pages 도메인
- `https://.*\.vercel\.app`: 모든 Vercel 프로덕션 도메인
- `https://.*-.*\.vercel\.app`: 모든 Vercel Preview 도메인 (하이픈 포함)

