import redis

# Redis 서버에 연결
try:
    cache = redis.Redis(host="localhost", port=6379, decode_responses=True)
    cache.ping()  # 연결 확인
    print("✅ Redis 연결 성공")
except redis.exceptions.ConnectionError:
    print("❌ Redis 연결 실패! Redis 서버를 실행하세요.")