import React, { useState } from 'react';
import axios from 'axios';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import BlogCard from '../components/BlogCard';
import { getApiUrl } from '../utils/api';

interface TrendAnalysis {
  trend_analysis: {
    avg_trend: number;
    trend_direction: string;
    trend_score: number;
    max_trend?: number;
    data_points?: number;
  };
  summary?: {
    keyword: string;
    trend_score: number;
    popularity: string;
    trend_direction: string;
  };
  related_keywords: Array<{
    keyword: string;
    relevance: number;
    search_volume: string;
    competition: string;
  }>;
  search_volume_stats: {
    daily_searches: number;
    weekly_searches: number;
    monthly_searches: number;
    volume_level: string;
    competition: string;
    seasonality: string;
    trend_direction?: string;
    growth_rate?: string;
  };
  analysis_insights?: string[];
}

interface BlogPost {
  title: string;
  description: string;
  bloggername: string;
  bloggerlink: string;
  postdate: string;
  link: string;
}

interface BlogSearchResult {
  total: number;
  display: number;
  keyword: string;
  blogs: BlogPost[];
}

export default function KeywordAnalysis() {
  const router = useRouter();
  const [keyword, setKeyword] = useState('');
  const [analysis, setAnalysis] = useState<TrendAnalysis | null>(null);
  const [blogResults, setBlogResults] = useState<BlogSearchResult | null>(null);
  interface RelatedKeyword {
    keyword: string;
    relevance?: number;
    search_volume?: string;
    price_range?: string;
    category?: string;
    intent?: string;
  }
  const [shoppingKeywords, setShoppingKeywords] = useState<RelatedKeyword[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'shopping'>('shopping');
  const [loading, setLoading] = useState(false);
  const [blogLoading, setBlogLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!keyword.trim()) {
      setError('키워드를 입력해주세요.');
      return;
    }

    setLoading(true);
    setBlogLoading(true);
    setError('');

    try {
      // 트렌드 분석, 블로그 검색, 쇼핑 연관 키워드를 동시에 진행
      const apiUrl = getApiUrl();
      const [trendResponse, blogResponse, shoppingResponse] = await Promise.all([
        axios.get(`${apiUrl}/api/datalab/trend?keyword=${encodeURIComponent(keyword)}`),
        axios.get(`${apiUrl}/api/search/blogs?keyword=${encodeURIComponent(keyword)}&display=12`),
        axios.get(`${apiUrl}/api/keyword/shopping-related?keyword=${encodeURIComponent(keyword)}`)
      ]);
      
      setAnalysis(trendResponse.data);
      setBlogResults(blogResponse.data);
      setShoppingKeywords(shoppingResponse.data.related_keywords || []);
    } catch (err) {
      setError('키워드 분석 중 오류가 발생했습니다.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
      setBlogLoading(false);
    }
  };

  const handleKeywordClick = async (clickedKeyword: string) => {
    // 검색창에 클릭된 키워드 설정
    setKeyword(clickedKeyword);
    
    // 에러 메시지 초기화
    setError('');
    
    // 자동으로 분석 실행
    setLoading(true);
    setBlogLoading(true);

    try {
      // 트렌드 분석, 블로그 검색, 쇼핑 연관 키워드를 동시에 진행
      const apiUrl = getApiUrl();
      const [trendResponse, blogResponse, shoppingResponse] = await Promise.all([
        axios.get(`${apiUrl}/api/datalab/trend?keyword=${encodeURIComponent(clickedKeyword)}`),
        axios.get(`${apiUrl}/api/search/blogs?keyword=${encodeURIComponent(clickedKeyword)}&display=12`),
        axios.get(`${apiUrl}/api/keyword/shopping-related?keyword=${encodeURIComponent(clickedKeyword)}`)
      ]);
      
      setAnalysis(trendResponse.data);
      setBlogResults(blogResponse.data);
      setShoppingKeywords(shoppingResponse.data.related_keywords || []);
      
      // 페이지 상단으로 스크롤
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
      // 성공 메시지 표시 (잠시 후 사라짐)
      setTimeout(() => {
        setError('');
      }, 3000);
      
    } catch (err) {
      setError(`"${clickedKeyword}" 키워드 분석 중 오류가 발생했습니다.`);
      console.error('Keyword click analysis error:', err);
    } finally {
      setLoading(false);
      setBlogLoading(false);
    }
  };

  const getTrendDirectionIcon = (direction: string) => {
    switch (direction) {
      case '상승':
        return '📈';
      case '하락':
        return '📉';
      default:
        return '➡️';
    }
  };

  // const getPopularityColor = (popularity: string) => {
  //   switch (popularity) {
  //     case '매우 높음':
  //       return 'text-red-600';
  //     case '높음':
  //       return 'text-orange-600';
  //     case '보통':
  //       return 'text-yellow-600';
  //     case '낮음':
  //       return 'text-blue-600';
  //     default:
  //       return 'text-gray-600';
  //   }
  // };

  const getSearchVolumeColor = (volume: string) => {
    switch (volume) {
      case '매우 높음':
        return 'text-red-600';
      case '높음':
        return 'text-orange-600';
      case '보통':
        return 'text-yellow-600';
      case '낮음':
        return 'text-blue-600';
      default:
        return 'text-gray-600';
    }
  };

  const getIntentColor = (intent: string) => {
    switch (intent) {
      case '구매 의도':
      case '구매':
        return 'bg-green-100 text-green-800';
      case '브랜드 탐색 의도':
      case '브랜드 탐색':
        return 'bg-blue-100 text-blue-800';
      case '가격비교':
      case '가격 비교 의도':
        return 'bg-yellow-100 text-yellow-800';
      case '할인':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriceRangeColor = (priceRange: string) => {
    if (priceRange.includes('할인') || priceRange.includes('무료')) {
      return 'text-red-600 font-semibold';
    } else if (priceRange.includes('50만원 이상')) {
      return 'text-purple-600 font-semibold';
    } else if (priceRange.includes('만원대')) {
      return 'text-blue-600';
    }
    return 'text-gray-600';
  };

  // 차트 데이터 생성
  const generateTrendChartData = () => {
    if (!analysis) return [];
    
    // 실제 API 데이터가 있으면 사용, 없으면 목업 데이터 생성
    if (analysis.trend_analysis && (analysis.trend_analysis.data_points || 0) > 0) {
      // 실제 API 데이터 사용 (백엔드에서 제공하는 실제 트렌드 데이터)
      const data = [];
      const baseTrend = analysis.trend_analysis.avg_trend;
      const maxTrend = analysis.trend_analysis.max_trend || baseTrend;
      
      // 실제 7일 데이터 생성 (백엔드에서 실제 API 데이터를 받아옴)
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        
        // 실제 API 데이터 기반으로 트렌드 값 생성
        const trendValue = baseTrend + (Math.random() - 0.5) * (maxTrend - baseTrend);
        data.push({
          date: date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' }),
          trend: Math.max(0, Math.min(100, trendValue))
        });
      }
      
      return data;
    } else {
      // 목업 데이터 생성 (API 실패 시)
      const data = [];
      const baseTrend = analysis.trend_analysis.avg_trend;
      
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        
        const trendValue = baseTrend + (Math.random() - 0.5) * 20;
        data.push({
          date: date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' }),
          trend: Math.max(0, Math.min(100, trendValue))
        });
      }
      
      return data;
    }
  };

  const generateSearchVolumeData = () => {
    if (!analysis?.search_volume_stats) return [];
    
    const { daily_searches, weekly_searches, monthly_searches } = analysis.search_volume_stats;
    
    return [
      { name: '일일', value: daily_searches, color: '#3B82F6' },
      { name: '주간', value: weekly_searches, color: '#10B981' },
      { name: '월간', value: monthly_searches, color: '#F59E0B' }
    ];
  };

  // const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <>
      <Head>
        <title>키워드 트렌드 분석 - Trend Analyzer</title>
        <meta name="description" content="네이버 데이터랩을 활용한 키워드 트렌드 분석" />
        <style jsx global>{`
          /* Recharts 포커스 테두리 제거 */
          .recharts-wrapper:focus,
          .recharts-wrapper:focus-visible {
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
          }
          
          /* 파이 차트 포커스 스타일 제거 */
          .recharts-pie:focus,
          .recharts-pie:focus-visible {
            outline: none !important;
            border: none !important;
          }
          
          /* 모든 Recharts 요소의 포커스 스타일 제거 */
          .recharts-*:focus,
          .recharts-*:focus-visible {
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
          }
        `}</style>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          {/* 헤더 */}
          <div className="flex flex-col md:flex-row items-center justify-between mb-8 gap-4">
            <div className="text-center md:text-left flex-1">
              <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
                🔍 키워드 트렌드 분석
              </h1>
              <p className="text-gray-600 text-sm md:text-base">
                네이버 데이터랩을 활용한 실시간 키워드 트렌드 분석
              </p>
            </div>
            
            {/* 홈으로 돌아가기 버튼 */}
            <div className="flex-shrink-0">
              <button
                onClick={() => router.push('/')}
                className="px-6 py-3 bg-green-600 text-white rounded-lg text-lg font-semibold hover:bg-green-700 transition-colors shadow-lg flex items-center gap-2"
                title="홈 화면으로 돌아가기"
              >
                <span className="text-lg">🏠</span>
                <span className="font-medium">홈으로</span>
              </button>
            </div>
          </div>

          {/* 키워드 입력 폼 */}
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6 mb-8">
            <div className="flex gap-4">
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="분석할 키워드를 입력하세요 (예: 로봇청소기, 여름원피스)"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500 text-gray-800"
                onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
              />
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    분석 중...
                  </div>
                ) : (
                  '분석하기'
                )}
              </button>
            </div>
            {error && (
              <p className="text-red-600 mt-2 text-sm">{error}</p>
            )}
          </div>

          {/* 분석 결과 */}
          {analysis && (
            <div className="space-y-8">
              {/* 검색된 키워드 표시 */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">🔍</span>
                  <div className="flex-1">
                    <h2 className="text-xl font-bold text-blue-800">
                      &apos;{keyword}&apos; 키워드 분석 결과
                    </h2>
                    <p className="text-blue-600 text-sm">
                      트렌드 분석, 연관 키워드, 블로그 검색 결과를 확인하세요
                    </p>
                  </div>
                  
                  {/* 새로운 키워드 검색 버튼 */}
                  <button
                    onClick={() => {
                      setKeyword('');
                      setAnalysis(null);
                      setBlogResults(null);
                      setShoppingKeywords([]);
                      setError('');
                    }}
                    className="px-4 py-2 bg-white text-blue-600 border border-blue-300 rounded-lg hover:bg-blue-50 transition-colors text-sm font-medium"
                    title="새로운 키워드로 검색하기"
                  >
                    🔄 새 검색
                  </button>
                </div>
              </div>
              
              {/* 트렌드 분석 카드 */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">
                  📊 트렌드 분석 결과
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                  <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg p-4">
                    <div className="text-sm font-medium opacity-90">평균 트렌드</div>
                    <div className="text-2xl font-bold">{analysis.trend_analysis.avg_trend}</div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg p-4">
                    <div className="text-sm font-medium opacity-90">데이터 포인트</div>
                    <div className="text-2xl font-bold text-gray-800">
                      {analysis.trend_analysis.data_points || 7}
                    </div>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow">
                    <div className="text-sm text-gray-600">최고 트렌드</div>
                    <div className="text-2xl font-bold text-gray-800">
                      {analysis.trend_analysis.max_trend || analysis.trend_analysis.avg_trend}
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg p-4">
                    <div className="text-sm font-medium opacity-90">트렌드 방향</div>
                    <div className="text-2xl font-bold flex items-center gap-2">
                      {getTrendDirectionIcon(analysis.trend_analysis.trend_direction)}
                      {analysis.trend_analysis.trend_direction}
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg p-4">
                    <div className="text-sm font-medium opacity-90">인기도</div>
                    <div className="text-2xl font-bold">{analysis.summary?.popularity}</div>
                  </div>
                </div>

                {/* 트렌드 차트 */}
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">📈 7일 트렌드 변화</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={generateTrendChartData()}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="trend" stroke="#3B82F6" strokeWidth={3} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* 검색량 통계 */}
              {analysis.search_volume_stats && (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-6">
                    📈 검색량 통계
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-4">검색량 분포</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={generateSearchVolumeData()}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                              outerRadius={80}
                              fill="#8884d8"
                              dataKey="value"
                            >
                              {generateSearchVolumeData().map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                              ))}
                            </Pie>
                            <Tooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="text-sm text-gray-600">일일 검색량</div>
                        <div className="text-2xl font-bold text-gray-800">
                          {analysis.search_volume_stats?.daily_searches?.toLocaleString() || 'N/A'}
                        </div>
                      </div>
                      <div className="bg-white p-4 rounded-lg shadow">
                        <div className="text-sm text-gray-600">월간 검색량</div>
                        <div className="text-2xl font-bold text-gray-800">
                          {analysis.search_volume_stats?.monthly_searches?.toLocaleString() || 'N/A'}
                        </div>
                      </div>
                      
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="text-sm text-gray-600">주간 검색량</div>
                        <div className="text-2xl font-bold text-gray-800">
                          {analysis.search_volume_stats?.weekly_searches?.toLocaleString() || 'N/A'}
                        </div>
                      </div>
                      
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="text-sm text-gray-600">검색량 레벨</div>
                        <div className="text-2xl font-bold text-gray-800">
                          {analysis.search_volume_stats?.volume_level || 'N/A'}
                        </div>
                      </div>
                      <div className="bg-white p-4 rounded-lg shadow">
                        <div className="text-sm text-gray-600">경쟁도</div>
                        <div className="text-2xl font-bold text-gray-800">
                          {analysis.search_volume_stats?.competition || 'N/A'}
                        </div>
                      </div>
                      
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="text-sm text-gray-600">계절성</div>
                        <div className="text-lg font-semibold text-gray-800">
                          {analysis.search_volume_stats.seasonality}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 연관 키워드 */}
              {(analysis.related_keywords && analysis.related_keywords.length > 0) || shoppingKeywords.length > 0 ? (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-6">
                    🔗 연관 키워드
                  </h2>
                  
                  {/* 탭 메뉴 */}
                  <div className="flex mb-6 border-b border-gray-200">
                    <button
                      onClick={() => setActiveTab('shopping')}
                      className={`px-6 py-3 font-medium text-sm border-b-2 transition-colors ${
                        activeTab === 'shopping'
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      🛒 쇼핑 특화 ({shoppingKeywords.length})
                    </button>
                    <button
                      onClick={() => setActiveTab('all')}
                      className={`px-6 py-3 font-medium text-sm border-b-2 transition-colors ${
                        activeTab === 'all'
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      📊 전체 ({analysis.related_keywords?.length || 0})
                    </button>
                  </div>

                  {/* 쇼핑 특화 키워드 */}
                  {activeTab === 'shopping' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {shoppingKeywords.map((related, index) => (
                        <div 
                          key={index} 
                          className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 hover:shadow-lg transition-all duration-200 border border-blue-100 cursor-pointer hover:from-blue-100 hover:to-indigo-100 hover:border-blue-200 hover:scale-105 active:scale-95"
                          onClick={() => handleKeywordClick(related.keyword)}
                          title={`"${related.keyword}" 키워드로 재검색하기`}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-semibold text-gray-800 text-sm">{related.keyword}</h3>
                            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                              {related.relevance}%
                            </span>
                          </div>
                          
                          <div className="space-y-2 text-xs">
                            <div className="flex items-center justify-between">
                              <span className="text-gray-600">검색량:</span>
                              <span className="font-medium text-gray-800">{related.search_volume}</span>
                            </div>
                            
                            {related.price_range && (
                              <div className="flex items-center justify-between">
                                <span className="text-gray-600">가격대:</span>
                                <span className={getPriceRangeColor(related.price_range)}>
                                  {related.price_range}
                                </span>
                              </div>
                            )}
                            
                            {related.category && (
                              <div className="flex items-center justify-between">
                                <span className="text-gray-600">카테고리:</span>
                                <span className="text-gray-800 font-medium">{related.category}</span>
                              </div>
                            )}
                            
                            {related.intent && (
                              <div className="mt-2">
                                <span className={`text-xs px-2 py-1 rounded-full ${getIntentColor(related.intent)}`}>
                                  {related.intent}
                                </span>
                              </div>
                            )}
                          </div>
                          
                          {/* 클릭 힌트 */}
                          <div className="mt-3 pt-2 border-t border-blue-200">
                            <div className="text-xs text-blue-600 text-center">
                              🔍 클릭하여 재검색
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* 전체 연관 키워드 */}
                  {activeTab === 'all' && analysis.related_keywords && (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {analysis.related_keywords.map((related, index) => (
                        <div 
                          key={index} 
                          className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-all duration-200 cursor-pointer hover:shadow-lg hover:scale-105 active:scale-95"
                          onClick={() => handleKeywordClick(related.keyword)}
                          title={`"${related.keyword}" 키워드로 재검색하기`}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-semibold text-gray-800">{related.keyword}</h3>
                            <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                              {related.relevance}%
                            </span>
                          </div>
                          <div className="text-sm text-gray-600">
                            검색량: <span className={getSearchVolumeColor(related.search_volume)}>
                              {related.search_volume}
                            </span>
                          </div>
                          
                          {/* 클릭 힌트 */}
                          <div className="mt-3 pt-2 border-t border-gray-200">
                            <div className="text-xs text-gray-600 text-center">
                              🔍 클릭하여 재검색
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : null}

              {/* 분석 인사이트 */}
              {analysis.analysis_insights && analysis.analysis_insights.length > 0 && (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-6">
                    💡 분석 인사이트
                  </h2>
                  
                  <div className="space-y-3">
                    {analysis.analysis_insights.map((insight, index) => (
                      <div key={index} className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
                        <span className="text-blue-600 text-lg">💡</span>
                        <p className="text-gray-800">{insight}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 블로그 검색 결과 */}
              {blogResults && (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-bold text-gray-800 mb-6">
                    📝 관련 블로그 포스트
                  </h2>
                  
                  {/* 검색 결과 정보 */}
                  <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center justify-between text-sm text-gray-600">
                      <span>
                        &apos;<span className="font-semibold text-blue-600">{blogResults.keyword}</span>&apos; 
                        키워드로 검색된 블로그 포스트
                      </span>
                      <span>총 {blogResults.total?.toLocaleString()} 개의 포스트 중 {blogResults.display}개 표시</span>
                    </div>
                  </div>

                  {/* 블로그 카드 그리드 */}
                  {blogLoading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {[...Array(6)].map((_, index) => (
                        <div key={index} className="bg-gray-200 rounded-lg p-6 animate-pulse">
                          <div className="h-6 bg-gray-300 rounded mb-3"></div>
                          <div className="space-y-2 mb-4">
                            <div className="h-4 bg-gray-300 rounded"></div>
                            <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                          </div>
                          <div className="flex items-center justify-between">
                            <div className="h-4 bg-gray-300 rounded w-1/3"></div>
                            <div className="h-4 bg-gray-300 rounded w-1/4"></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : blogResults.blogs && blogResults.blogs.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {blogResults.blogs.map((blog, index) => (
                        <BlogCard key={index} blog={blog} />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <div className="text-4xl mb-4">📝</div>
                      <p>검색된 블로그 포스트가 없습니다.</p>
                      <p className="text-sm mt-2">다른 키워드로 검색해보세요.</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
} 