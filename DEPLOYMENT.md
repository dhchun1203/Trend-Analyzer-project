# 🚀 배포 가이드

이 프로젝트를 배포하는 방법입니다.

## 📋 배포 전 준비사항

### 1. GitHub에 프로젝트 올리기

```bash
# Git 사용자 정보 설정 (아직 안 했다면)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 커밋 및 푸시
git add .
git commit -m "Initial commit: Trend Analyzer project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/trend_analyzer.git
git push -u origin main
```

## 🎯 배포 전략

이 프로젝트는 **프론트엔드(Next.js)**와 **백엔드(FastAPI)**로 구성되어 있어 각각 배포해야 합니다.

### 옵션 1: Vercel (프론트엔드) + Railway/Render (백엔드) - 권장 ⭐

### 옵션 2: Netlify (프론트엔드) + Railway/Render (백엔드)

### 옵션 3: GitHub Pages (정적 사이트만 가능, API 라우트 불가)

---

## 🌐 프론트엔드 배포 (Next.js)

### Vercel 사용 (가장 쉬움) ⭐

1. **Vercel 가입**: https://vercel.com
2. **GitHub 연동**: Vercel 대시보드에서 "New Project" → GitHub 저장소 선택
3. **프로젝트 설정**:
   - Root Directory: `frontend`
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. **환경 변수 설정**:
   - `NEXT_PUBLIC_API_URL`: 백엔드 API URL (예: `https://your-backend.railway.app`)
5. **Deploy** 클릭

### Netlify 사용

1. **Netlify 가입**: https://netlify.com
2. **GitHub 연동**: "New site from Git" → GitHub 저장소 선택
3. **빌드 설정**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/.next`
4. **환경 변수 설정**: `NEXT_PUBLIC_API_URL`

---

## 🔧 백엔드 배포 (FastAPI)

### Railway 사용 (권장) ⭐

1. **Railway 가입**: https://railway.app
2. **GitHub 연동**: "New Project" → "Deploy from GitHub repo" → 저장소 선택
3. **서비스 설정**:
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **환경 변수 설정**:
   - `MONGO_URI`: MongoDB 연결 문자열 (있는 경우)
   - 네이버 API 키들 (`.env` 파일에 있던 것들)
5. **배포**: 자동으로 배포됩니다

### Render 사용

1. **Render 가입**: https://render.com
2. **"New Web Service"** 클릭
3. **GitHub 저장소 연결**
4. **설정**:
   - Name: `trend-analyzer-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend`
5. **환경 변수 추가**
6. **Deploy** 클릭

---

## ⚙️ 배포 후 설정

### 프론트엔드 환경 변수 수정

배포된 백엔드 URL을 프론트엔드에 설정해야 합니다.

1. **Vercel/Netlify 환경 변수**:
   - `NEXT_PUBLIC_API_URL`: 백엔드 URL (예: `https://your-backend.railway.app`)

2. **프론트엔드 코드 수정**: ✅ 완료
   - 모든 API 호출이 환경 변수(`NEXT_PUBLIC_API_URL`)를 사용하도록 수정됨
   - `frontend/utils/api.ts`에서 중앙 관리

---

## 📝 체크리스트

- [ ] GitHub에 프로젝트 업로드 완료
- [ ] 백엔드 배포 (Railway/Render)
- [ ] 백엔드 URL 확인
- [ ] 프론트엔드 배포 (Vercel/Netlify)
- [ ] 환경 변수 설정
- [ ] 프론트엔드에서 백엔드 URL 수정
- [ ] 배포된 사이트 테스트

---

## 🔗 유용한 링크

- [Vercel 배포 가이드](https://vercel.com/docs)
- [Railway 배포 가이드](https://docs.railway.app)
- [Render 배포 가이드](https://render.com/docs)
- [Next.js 배포 문서](https://nextjs.org/docs/deployment)

