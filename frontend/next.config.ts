import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  // Vercel 배포를 위한 설정
  // output: 'export' 제거 (Vercel은 SSR/SSG 지원)
  // basePath 제거 (Vercel은 루트 도메인 사용)
  // 이미지 최적화 활성화 (Vercel은 이미지 최적화 지원)
  images: {
    // Vercel의 이미지 최적화 사용
    domains: [],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
};

export default nextConfig;
