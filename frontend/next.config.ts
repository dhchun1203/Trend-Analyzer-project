import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  // GitHub Pages 배포를 위한 설정
  output: 'export',
  // GitHub Pages는 /repository-name 경로를 사용하므로 basePath 설정
  // 저장소 이름: Trend-Analyzer-project
  basePath: (process.env.NEXT_PUBLIC_BASE_PATH && process.env.NEXT_PUBLIC_BASE_PATH.startsWith('/')) 
    ? process.env.NEXT_PUBLIC_BASE_PATH 
    : '/Trend-Analyzer-project',
  // 이미지 최적화 비활성화 (정적 export에서는 제한적)
  images: {
    unoptimized: true,
  },
  // API 라우트는 정적 export에서 무시됨 (경고 방지)
  experimental: {
    // API 라우트 관련 경고 무시
  },
};

export default nextConfig;
