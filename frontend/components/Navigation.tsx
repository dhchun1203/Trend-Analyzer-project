import React, { useState } from 'react';
import Link from 'next/link';

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* 로고 */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">📊</span>
            <span className="text-lg sm:text-xl font-bold text-gray-800">Trend Analyzer</span>
          </Link>

          {/* 데스크톱 네비게이션 링크 */}
          <div className="hidden md:flex space-x-4 lg:space-x-8">
            <Link href="/" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              🏠 홈
            </Link>
            <Link href="/categories" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              📂 카테고리별 상품
            </Link>
            <Link href="/keyword-analysis" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              🔍 키워드 분석
            </Link>
            <Link href="/test-api" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              🧪 API 테스트
            </Link>
          </div>

          {/* 모바일 메뉴 버튼 */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="메뉴 열기"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* 모바일 메뉴 */}
        <div 
          className={`md:hidden border-t border-gray-200 overflow-hidden transition-all duration-300 ease-in-out ${
            mobileMenuOpen ? 'max-h-96 opacity-100 py-4' : 'max-h-0 opacity-0 py-0'
          }`}
        >
          <div className={`flex flex-col space-y-2 transition-transform duration-300 ease-in-out ${
            mobileMenuOpen ? 'translate-y-0' : '-translate-y-4'
          }`}>
              <Link 
                href="/" 
                className={`text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-4 py-2 rounded-md text-base font-medium transition-all duration-300 ${
                  mobileMenuOpen ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
                }`}
                style={{ transitionDelay: mobileMenuOpen ? '0.1s' : '0s' }}
                onClick={() => setMobileMenuOpen(false)}
              >
                🏠 홈
              </Link>
              <Link 
                href="/categories" 
                className={`text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-4 py-2 rounded-md text-base font-medium transition-all duration-300 ${
                  mobileMenuOpen ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
                }`}
                style={{ transitionDelay: mobileMenuOpen ? '0.15s' : '0s' }}
                onClick={() => setMobileMenuOpen(false)}
              >
                📂 카테고리별 상품
              </Link>
              <Link 
                href="/keyword-analysis" 
                className={`text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-4 py-2 rounded-md text-base font-medium transition-all duration-300 ${
                  mobileMenuOpen ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
                }`}
                style={{ transitionDelay: mobileMenuOpen ? '0.2s' : '0s' }}
                onClick={() => setMobileMenuOpen(false)}
              >
                🔍 키워드 분석
              </Link>
              <Link 
                href="/test-api" 
                className={`text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-4 py-2 rounded-md text-base font-medium transition-all duration-300 ${
                  mobileMenuOpen ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
                }`}
                style={{ transitionDelay: mobileMenuOpen ? '0.25s' : '0s' }}
                onClick={() => setMobileMenuOpen(false)}
              >
                🧪 API 테스트
              </Link>
          </div>
        </div>
      </div>
    </nav>
  );
} 