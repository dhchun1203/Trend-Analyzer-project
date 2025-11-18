import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  // rewrites는 제거 - pages/api/crawl.ts에서 직접 백엔드 호출
  // async rewrites() {
  //   return [
  //     {
  //       source: "/api/crawl",
  //       destination: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/crawl",
  //     },
  //   ];
  // },
};

export default nextConfig;
