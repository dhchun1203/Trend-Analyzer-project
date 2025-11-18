import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/crawl",
        destination: "http://localhost:8000/crawl",
      },
    ];
  },
};

export default nextConfig;
