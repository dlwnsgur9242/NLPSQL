import redis
import hashlib
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

# ✅ Redis 연결 설정
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def hash_query(query):
    """질의를 해시값으로 변환하여 캐싱 키 생성"""
    return hashlib.md5(query.encode()).hexdigest()

def get_sql_from_cache(query):
    """캐싱된 SQL 조회"""
    cache_key = hash_query(query)
    cached_sql = cache.get(cache_key)
    return cached_sql.decode() if cached_sql else None

def store_sql_to_cache(query, sql):
    """SQL을 캐싱하여 저장 (1시간 유지)"""
    cache_key = hash_query(query)
    cache.setex(cache_key, 3600, sql)

# ✅ 테스트 실행
if __name__ == "__main__":
    query = "천안에 있는 태양광 발전소를 보여줘"
    store_sql_to_cache(query, "SELECT * FROM tm_event WHERE location = '천안';")
    print("🔄 캐싱된 SQL:", get_sql_from_cache(query))
