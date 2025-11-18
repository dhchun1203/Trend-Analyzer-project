import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = None
db = None
collection = None
MONGODB_AVAILABLE = False

# MongoDB 연결 시도 (실패해도 서버는 시작 가능)
if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # 연결 테스트
        client.server_info()
        db = client['trend_db']
        collection = db['naver_best100']
        MONGODB_AVAILABLE = True
        print("✅ MongoDB 연결 성공!")
    except Exception as e:
        print(f"⚠️ MongoDB 연결 실패 (서버는 계속 실행됩니다): {e}")
        MONGODB_AVAILABLE = False
else:
    print("⚠️ MONGO_URI 환경 변수가 설정되지 않았습니다. MongoDB 기능이 비활성화됩니다.")
