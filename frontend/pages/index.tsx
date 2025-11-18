import axios from "axios";
import { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";
import Navigation from "../components/Navigation";
import Link from "next/link";
import { getApiUrl } from "../utils/api";

interface Product {
  rank: number;
  product_name: string;
  price: string;
  product_url: string;
  image_url: string;
  mall_name: string;
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 백엔드 API 직접 호출 (GitHub Pages 호환)
        const apiUrl = getApiUrl();
        const res = await axios.get(`${apiUrl}/api/popular-products`);
        setProducts(res.data.items || []);
      } catch (error) {
        console.error('상품 데이터 로드 실패:', error);
      }
    };
    fetchData();
  }, []);

  return (
    <>
      <Navigation />
      <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="max-w-7xl mx-auto px-6 py-12">
          {/* 헤더 섹션 */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-red-500 via-orange-500 to-red-600 bg-clip-text text-transparent mb-4">
              🛍️ 인기상품 모음
            </h1>
            <p className="text-gray-600 text-lg mb-6">
              네이버 쇼핑의 인기 상품들을 카테고리별로 확인하세요
            </p>
            <Link 
              href="/keyword-analysis"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
            >
              🔍 키워드 트렌드 분석하기
            </Link>
          </div>

        {/* 상품 그리드 */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-5 gap-6 md:gap-8">
          {products.map((item) => (
            <div key={item.rank} className="mb-8 md:mb-12 bg-white rounded-lg p-2 shadow-sm product-card">
              <ProductCard
                imageUrl={item.image_url}
                productName={item.product_name}
                price={item.price}
                mallName={item.mall_name}
                productUrl={item.product_url}
                rank={item.rank}
              />
            </div>
          ))}
        </div>

        {/* 하단 여백 */}
        <div className="h-8"></div>
      </div>
    </main>
    </>
  );
}
