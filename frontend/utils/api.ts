// API URL 유틸리티
export const getApiUrl = (): string => {
  // 환경 변수가 있으면 사용, 없으면 localhost (개발 환경)
  return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
};

