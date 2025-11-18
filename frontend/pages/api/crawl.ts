import type { NextApiRequest, NextApiResponse } from "next";

type Product = {
  rank: number;
  product_name: string;
  price: string;
  product_url: string;
  image_url: string;
  mall_name: string;
  category: string;
  keyword?: string;
};

type Data = {
  items: Product[];
  count: number;
  categories?: string[];
};

type ErrorResponse = {
  error: string;
  details?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data | ErrorResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // 타임아웃을 위한 AbortController 생성
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10초 타임아웃
    
    // 새로운 인기상품 API 호출 (크롤링 대체)
    const response = await fetch('http://localhost:8000/api/popular-products', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Backend API error: ${response.status} - ${errorText}`);
      throw new Error(`Backend API error: ${response.status}`);
    }

    const data = await response.json();
    
    // 응답 데이터 검증
    if (!data.items || !Array.isArray(data.items)) {
      throw new Error('Invalid data format from backend');
    }

    res.status(200).json(data);
  } catch (error: any) {
    console.error('Popular Products API error:', error);
    
    // 더 자세한 에러 메시지
    const errorMessage = error.code === 'ECONNREFUSED' 
      ? '백엔드 서버에 연결할 수 없습니다. 백엔드 서버가 http://localhost:8000에서 실행 중인지 확인해주세요.'
      : error.message || '인기상품 서비스에 연결할 수 없습니다.';
    
    res.status(500).json({ 
      error: errorMessage,
      details: error.code || 'Unknown error'
    });
  }
} 