# GitHub Pages 배포 가이드

## 📋 사전 준비

1. GitHub 저장소의 Settings → Pages에서:
   - Source: "GitHub Actions" 선택

## 🚀 배포 방법

### 자동 배포 (권장)

1. GitHub 저장소 Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. 다음 환경 변수 추가:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://trend-analyzer-project-production.up.railway.app`
4. `main` 브랜치에 푸시하면 자동으로 배포됩니다

### 수동 배포

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=https://trend-analyzer-project-production.up.railway.app npm run build
```

빌드된 파일은 `frontend/out` 디렉토리에 생성됩니다.

## ⚙️ 설정

### basePath 설정

저장소 이름이 `trend_analyzer`인 경우:
- GitHub Pages URL: `https://username.github.io/trend_analyzer/`
- `next.config.ts`의 `basePath`를 `/trend_analyzer`로 설정

저장소 이름이 사용자명과 같거나 루트에 배포하는 경우:
- GitHub Pages URL: `https://username.github.io/`
- `basePath`를 빈 문자열로 설정 (현재 설정)

## 📝 주의사항

1. **API 라우트 미지원**: GitHub Pages는 정적 사이트만 지원하므로 `pages/api` 디렉토리의 API 라우트는 작동하지 않습니다.
   - 해결: 클라이언트에서 직접 백엔드 API 호출 (이미 수정됨)

2. **환경 변수**: GitHub Actions Secrets에 `NEXT_PUBLIC_API_URL` 설정 필요

3. **basePath**: 저장소 이름에 맞게 `next.config.ts`의 `basePath` 수정 필요

## 🔗 배포 후 확인

배포가 완료되면:
- `https://username.github.io/repository-name/` 접속
- 사이트가 정상 작동하는지 확인

