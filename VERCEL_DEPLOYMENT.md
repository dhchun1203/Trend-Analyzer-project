# Vercel 배포 가이드

## 📋 사전 준비

1. Vercel 계정 생성: https://vercel.com
2. GitHub 저장소와 Vercel 계정 연동

## 🚀 배포 방법

### 방법 1: Vercel 웹 대시보드에서 배포 (권장)

1. **프로젝트 가져오기**
   - Vercel 대시보드 접속
   - "Add New..." → "Project" 클릭
   - GitHub 저장소 선택
   - 저장소: `dhchun1203/Trend-Analyzer-project` 선택

2. **프로젝트 설정**
   - **Framework Preset**: Next.js (자동 감지)
   - **Root Directory**: `frontend` 선택
   - **Build Command**: `npm run build` (자동 설정됨)
   - **Output Directory**: `.next` (자동 설정됨)
   - **Install Command**: `npm install` (자동 설정됨)

3. **환경 변수 설정**
   - "Environment Variables" 섹션에서 다음 변수 추가:
     - **Name**: `NEXT_PUBLIC_API_URL`
     - **Value**: `https://trend-analyzer-project-production.up.railway.app`
     - **Environment**: Production, Preview, Development 모두 선택

4. **배포 실행**
   - "Deploy" 버튼 클릭
   - 배포 완료까지 대기 (약 2-3분)

### 방법 2: Vercel CLI를 통한 배포

1. **Vercel CLI 설치**
```bash
npm i -g vercel
```

2. **로그인**
```bash
vercel login
```

3. **프로젝트 배포**
```bash
cd frontend
vercel
```

4. **환경 변수 설정**
```bash
vercel env add NEXT_PUBLIC_API_URL
# 프롬프트에 따라 값 입력: https://trend-analyzer-project-production.up.railway.app
```

5. **프로덕션 배포**
```bash
vercel --prod
```

## ⚙️ 설정 파일

### vercel.json
프로젝트 루트에 `vercel.json` 파일이 생성되어 있습니다:
- `framework`: Next.js 프레임워크 자동 감지
- **주의**: `rootDirectory`는 Vercel 대시보드에서 설정해야 합니다 (vercel.json에서는 지원하지 않음)

### next.config.ts
Vercel 배포를 위해 수정된 설정:
- `output: 'export'` 제거 (Vercel은 SSR/SSG 지원)
- `basePath` 제거 (Vercel은 루트 도메인 사용)
- 이미지 최적화 활성화

## 🔗 배포 후 확인

배포가 완료되면:
- Vercel이 자동으로 도메인 생성 (예: `your-project.vercel.app`)
- 커스텀 도메인 설정 가능 (Settings → Domains)
- 사이트가 정상 작동하는지 확인

## 🔄 자동 배포

GitHub 저장소와 연동하면:
- `main` 브랜치에 푸시할 때마다 자동 배포
- Pull Request 생성 시 Preview 배포
- 배포 상태는 GitHub 커밋에 표시됨

## 📝 주요 변경사항

### GitHub Pages → Vercel 전환

1. **정적 Export 제거**
   - GitHub Pages: `output: 'export'` 필요
   - Vercel: SSR/SSG 지원, export 불필요

2. **basePath 제거**
   - GitHub Pages: `/repository-name` 경로 필요
   - Vercel: 루트 도메인 사용

3. **이미지 최적화**
   - GitHub Pages: `unoptimized: true` 필요
   - Vercel: 자동 이미지 최적화 지원

4. **환경 변수**
   - GitHub Pages: GitHub Actions Secrets
   - Vercel: Vercel 대시보드 환경 변수

## 🎯 Vercel의 장점

1. **빠른 배포**: CDN 기반 글로벌 배포
2. **자동 HTTPS**: SSL 인증서 자동 설정
3. **이미지 최적화**: 자동 이미지 최적화 및 변환
4. **Preview 배포**: PR마다 미리보기 배포
5. **Analytics**: 내장 분석 도구
6. **Serverless Functions**: API 라우트 지원

## 🔧 문제 해결

### 빌드 오류
- Vercel 대시보드의 "Deployments" 탭에서 로그 확인
- 로컬에서 `npm run build` 테스트

### 환경 변수 오류
- Vercel 대시보드에서 환경 변수 확인
- `NEXT_PUBLIC_` 접두사 확인

### 이미지 로딩 오류
- `next.config.ts`의 `remotePatterns` 확인
- 이미지 도메인 추가 필요 시 설정 수정

## 📞 참고 자료

- [Vercel 공식 문서](https://vercel.com/docs)
- [Next.js 배포 가이드](https://nextjs.org/docs/deployment)
- [Vercel CLI 문서](https://vercel.com/docs/cli)

