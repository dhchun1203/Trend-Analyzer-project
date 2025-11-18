import { useState, useEffect } from "react";
import Head from "next/head";
import Navigation from "../components/Navigation";
import ProductCard from "../components/ProductCard";
import Link from "next/link";
import { getApiUrl } from "../utils/api";

interface Product {
  rank: number;
  product_name: string;
  price: string;
  product_url: string;
  image_url: string;
  mall_name: string;
  category: string;
  keyword?: string;
}

const categories = [
  { id: "가전제품", name: "🏠 가전제품", description: "로봇청소기, 에어프라이어, 공기청정기 등" },
  { id: "생활용품", name: "🧹 생활용품", description: "청소기, 선풍기, 가습기, 제습기 등" },
  { id: "주방용품", name: "🍳 주방용품", description: "전기밥솥, 믹서기, 블렌더, 토스터 등" },
  { id: "패션", name: "👗 패션", description: "여름옷, 가을옷, 운동화, 가방, 모자 등" },
  { id: "뷰티", name: "💄 뷰티", description: "화장품, 스킨케어, 헤어케어, 향수 등" }
];

export default function Categories() {
  const [selectedCategory, setSelectedCategory] = useState<string>("가전제품");
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCategoryProducts(selectedCategory);
  }, [selectedCategory]);

  const fetchCategoryProducts = async (category: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${getApiUrl()}/api/products/category/${category}`);
      if (response.ok) {
        const data = await response.json();
        setProducts(data.items || []);
      }
    } catch (error) {
      console.error('카테고리별 상품 조회 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>카테고리별 상품 - Trend Analyzer</title>
      </Head>

      <Navigation />
      
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 lg:py-12">
          {/* 헤더 섹션 */}
          <div className="text-center mb-8 sm:mb-12">
            <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-green-500 via-blue-500 to-purple-600 bg-clip-text text-transparent mb-3 sm:mb-4 px-2">
              📂 카테고리별 상품
            </h1>
            <p className="text-gray-600 text-sm sm:text-base lg:text-lg mb-4 sm:mb-6 px-4">
              관심 있는 카테고리를 선택하여 다양한 상품을 둘러보세요
            </p>
            <Link 
              href="/"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
            >
              🏠 홈으로 돌아가기
            </Link>
          </div>

          {/* 카테고리 선택 */}
          <div className="mb-8 sm:mb-12">
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 sm:gap-4">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`p-3 sm:p-4 md:p-6 rounded-lg border-2 transition-all duration-200 ${
                    selectedCategory === category.id
                      ? 'border-blue-500 bg-blue-50 shadow-lg scale-105'
                      : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-xl sm:text-2xl mb-1 sm:mb-2">{category.name.split(' ')[0]}</div>
                    <div className="font-semibold text-gray-800 text-xs sm:text-sm md:text-base mb-1">
                      {category.name.split(' ').slice(1).join(' ')}
                    </div>
                    <div className="text-[10px] sm:text-xs text-gray-600 hidden sm:block">{category.description}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* 선택된 카테고리 상품 */}
          <div className="mb-8">
            <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6 px-2">
              {categories.find(c => c.id === selectedCategory)?.name} 상품
            </h2>
            
            {loading ? (
              <div className="text-center py-8 sm:py-12">
                <div className="animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600 text-sm sm:text-base">상품을 불러오는 중...</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-4 md:gap-6">
                {products.map((item) => (
                  <div key={item.rank} className="bg-white rounded-lg p-1 sm:p-2 shadow-sm product-card">
                    <ProductCard
                      imageUrl={item.image_url}
                      productName={item.product_name}
                      price={item.price}
                      mallName={item.mall_name}
                      productUrl={item.product_url}
                      rank={item.rank}
                    />
                    {item.keyword && (
                      <div className="text-xs text-blue-600 text-center mt-2 px-2 py-1 bg-blue-50 rounded">
                        #{item.keyword}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
} 