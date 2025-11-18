import React from 'react';

interface BlogPost {
  title: string;
  description: string;
  bloggername: string;
  bloggerlink: string;
  postdate: string;
  link: string;
}

interface BlogCardProps {
  blog: BlogPost;
}

export default function BlogCard({ blog }: BlogCardProps) {
  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    
    // YYYYMMDD 형식을 YYYY.MM.DD로 변환
    if (dateString.length === 8) {
      const year = dateString.substring(0, 4);
      const month = dateString.substring(4, 6);
      const day = dateString.substring(6, 8);
      return `${year}.${month}.${day}`;
    }
    
    return dateString;
  };

  const handleBlogClick = () => {
    if (blog.link) {
      window.open(blog.link, '_blank', 'noopener,noreferrer');
    }
  };

  const handleBloggerClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (blog.bloggerlink) {
      window.open(blog.bloggerlink, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer border border-gray-200 hover:border-blue-300 blog-card group"
      onClick={handleBlogClick}
    >
      {/* 블로그 제목 */}
      <h3 className="text-lg font-semibold text-gray-800 mb-3 line-clamp-2 hover:text-blue-600 transition-colors">
        {blog.title || '제목 없음'}
      </h3>
      
      {/* 블로그 내용 미리보기 */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed">
        {blog.description || '내용 미리보기가 없습니다.'}
      </p>
      
      {/* 블로그 정보 */}
      <div className="flex items-center justify-between text-sm text-gray-500">
        <div className="flex items-center gap-2">
          <span className="text-blue-600">📝</span>
          {blog.bloggername ? (
            <button
              onClick={handleBloggerClick}
              className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
            >
              {blog.bloggername}
            </button>
          ) : (
            <span className="text-gray-400">익명</span>
          )}
        </div>
        
        {blog.postdate && (
          <div className="flex items-center gap-1">
            <span className="text-gray-400">📅</span>
            <span>{formatDate(blog.postdate)}</span>
          </div>
        )}
      </div>
      
      {/* 호버 효과 표시 */}
      <div className="mt-3 pt-3 border-t border-gray-100 opacity-0 group-hover:opacity-100 transition-opacity">
        <span className="text-xs text-gray-400 flex items-center gap-1">
          <span>🔗</span>
          블로그 포스트 보러가기
        </span>
      </div>
    </div>
  );
} 