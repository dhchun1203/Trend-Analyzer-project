import React from 'react';

interface ProductCardProps {
  imageUrl: string;
  productName: string;
  price: string;
  mallName: string;
  productUrl: string;
  rank: number;
}

const ProductCard = ({
  imageUrl,
  productName,
  price,
  mallName,
  productUrl,
  rank,
}: ProductCardProps) => {
  return (
    <a
      href={productUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="group bg-white rounded-lg overflow-hidden shadow-md border border-gray-200 relative product-card"
    >
      {/* 순위 배지 */}
      <div className="absolute top-1 left-1 z-10 bg-gradient-to-r from-red-500 to-red-600 text-white text-xs font-bold px-1.5 py-0.5 rounded-full shadow-sm">
        {rank}
      </div>
      
      {/* 이미지 컨테이너 */}
      <div className="relative overflow-hidden">
        <img
          src={imageUrl}
          alt={productName}
          className="w-full h-40 object-cover transition-transform duration-200"
        />
        {/* 호버 오버레이 */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
      </div>
      
            {/* 콘텐츠 영역 */}
      <div className="p-3 bg-white min-h-[80px]">
          <h3 className="font-semibold text-gray-800 text-sm leading-tight line-clamp-2 mb-2 group-hover:text-blue-600 transition-colors">
            {productName}
          </h3>
          <p className="text-red-600 font-bold text-sm mb-1">{price}</p>
          <p className="text-gray-500 text-xs truncate">{mallName}</p>
        </div>
    </a>
  );
};


export default ProductCard;
