import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 연결
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
print(f"MongoDB URI: {MONGO_URI}")

try:
    client = MongoClient(MONGO_URI)
    db = client['trend_db']
    collection = db['naver_best100']
    
    # 전체 문서 수 확인
    total_count = collection.count_documents({})
    print(f"전체 문서 수: {total_count}")
    
    # 카테고리별 문서 수 확인
    category_count = collection.count_documents({"category": "전체"})
    print(f"'전체' 카테고리 문서 수: {category_count}")
    
    # 샘플 데이터 확인
    sample_data = list(collection.find({}).limit(3))
    print(f"\n샘플 데이터:")
    for i, doc in enumerate(sample_data, 1):
        print(f"{i}. {doc.get('product_name', 'N/A')} - {doc.get('price', 'N/A')}")
    
    client.close()
    print("\n데이터베이스 연결 성공!")
    
except Exception as e:
    print(f"데이터베이스 연결 오류: {e}")
    print("MongoDB가 실행 중인지 확인해주세요.") 