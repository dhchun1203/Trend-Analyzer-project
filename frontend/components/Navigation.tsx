import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

export default function Navigation() {
  // const router = useRouter(); // 향후 활성 링크 표시에 사용 예정

  // const isActive = (path: string) => {
  //   return router.pathname === path;
  // };

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* 로고 */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">📊</span>
            <span className="text-xl font-bold text-gray-800">Trend Analyzer</span>
          </Link>

          {/* 네비게이션 링크 */}
          <div className="hidden md:flex space-x-8">
            <Link href="/" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              🏠 홈
            </Link>
            <Link href="/categories" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              📂 카테고리별 상품
            </Link>
            <Link href="/keyword-analysis" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              🔍 키워드 분석
            </Link>
            <Link href="/test-api" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              🧪 API 테스트
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
} 