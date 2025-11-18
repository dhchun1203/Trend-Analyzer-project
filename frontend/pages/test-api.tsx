import React, { useState } from 'react';
import Head from 'next/head';
import { getApiUrl } from '../utils/api';

interface TestResult {
  success: boolean;
  data?: unknown;
  error?: string;
}

export default function TestAPI() {
  const [keyword, setKeyword] = useState('로봇청소기');
  const [results, setResults] = useState<{[key: string]: TestResult}>({});

  const testAPI = async (endpoint: string, description: string) => {
    try {
      const response = await fetch(`${getApiUrl()}${endpoint}`);
      const data = await response.json();
      
      setResults(prev => ({
        ...prev,
        [description]: { success: true, data }
      }));
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setResults(prev => ({
        ...prev,
        [description]: { 
          success: false, 
          error: errorMessage 
        }
      }));
    }
  };

  const testDatalabAPI = () => testAPI('/api/datalab/test', 'datalab');
  const testKeywordAnalysis = () => testAPI(`/api/datalab/trend?keyword=${encodeURIComponent(keyword)}`, 'keyword');
  const testRelatedKeywords = () => testAPI(`/api/datalab/related-keywords?keyword=${encodeURIComponent(keyword)}`, 'related');

  return (
    <>
      <Head>
        <title>API 테스트 - Trend Analyzer</title>
      </Head>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">🔧 API 테스트</h1>
            
            <div className="space-y-6">
              {/* 네이버 데이터랩 API 테스트 */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">1. 네이버 데이터랩 API 테스트</h3>
                <button 
                  onClick={testDatalabAPI}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
                >
                  데이터랩 API 테스트
                </button>
                {results.datalab && (
                  <div className={`mt-3 p-3 rounded ${results.datalab.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <h4 className={`font-semibold ${results.datalab.success ? 'text-green-800' : 'text-red-800'}`}>
                      {results.datalab.success ? '✅ 성공!' : '❌ 실패!'}
                    </h4>
                    <pre className="mt-2 text-sm overflow-x-auto">
                      {JSON.stringify(results.datalab.data || results.datalab.error, null, 2)}
                    </pre>
                  </div>
                )}
              </div>

              {/* 키워드 분석 API 테스트 */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">2. 키워드 분석 API 테스트</h3>
                <div className="flex gap-2 mb-3">
                  <input 
                    type="text" 
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    placeholder="테스트 키워드 입력"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button 
                    onClick={testKeywordAnalysis}
                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors"
                  >
                    키워드 분석 테스트
                  </button>
                </div>
                {results.keyword && (
                  <div className={`mt-3 p-3 rounded ${results.keyword.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <h4 className={`font-semibold ${results.keyword.success ? 'text-green-800' : 'text-red-800'}`}>
                      {results.keyword.success ? '✅ 성공!' : '❌ 실패!'}
                    </h4>
                    <pre className="mt-2 text-sm overflow-x-auto">
                      {JSON.stringify(results.keyword.data || results.keyword.error, null, 2)}
                    </pre>
                  </div>
                )}
              </div>

              {/* 연관 키워드 API 테스트 */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">3. 연관 키워드 API 테스트</h3>
                <button 
                  onClick={testRelatedKeywords}
                  className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition-colors"
                >
                  연관 키워드 테스트
                </button>
                {results.related && (
                  <div className={`mt-3 p-3 rounded ${results.related.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <h4 className={`font-semibold ${results.related.success ? 'text-green-800' : 'text-red-800'}`}>
                      {results.related.success ? '✅ 성공!' : '❌ 실패!'}
                    </h4>
                    <pre className="mt-2 text-sm overflow-x-auto">
                      {JSON.stringify(results.related.data || results.related.error, null, 2)}
                    </pre>
                  </div>
                )}
              </div>

              {/* 새로운 API 키 테스트 */}
              <div className="border border-gray-200 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">4. 새로운 API 키 테스트</h3>
                <div className="flex gap-2 mb-3">
                  <input 
                    type="text" 
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    placeholder="테스트 키워드 입력"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button 
                    onClick={() => testAPI(`/api/datalab/trend?keyword=${encodeURIComponent(keyword)}`, 'new-api')}
                    className="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700 transition-colors"
                  >
                    새 API 키 테스트
                  </button>
                </div>
                {results['new-api'] && (
                  <div className={`mt-3 p-3 rounded ${results['new-api'].success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <h4 className={`font-semibold ${results['new-api'].success ? 'text-green-800' : 'text-red-800'}`}>
                      {results['new-api'].success ? '✅ 새로운 API 키 성공!' : '❌ 새로운 API 키 실패!'}
                    </h4>
                    <pre className="mt-2 text-sm overflow-x-auto">
                      {JSON.stringify(results['new-api'].data || results['new-api'].error, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            </div>

            {/* 전체 결과 요약 */}
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">📊 테스트 결과 요약</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(results).map(([key, result]) => (
                  <div key={key} className={`p-3 rounded ${result.success ? 'bg-green-100' : 'bg-red-100'}`}>
                    <div className={`font-semibold ${result.success ? 'text-green-800' : 'text-red-800'}`}>
                      {key.charAt(0).toUpperCase() + key.slice(1)} API
                    </div>
                    <div className="text-sm">
                      {result.success ? '✅ 정상 작동' : '❌ 오류 발생'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
} 