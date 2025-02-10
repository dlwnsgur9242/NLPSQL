from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import connection_string
import urllib

# ✅ MSSQL 데이터베이스 연결 설정
params = urllib.parse.quote_plus(connection_string)
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_url)

# ✅ 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def execute_sql(query):
    """변환된 SQL을 MSSQL에서 실행하고 결과를 반환"""
    with SessionLocal() as session:
        result = session.execute(text(query))
        return [dict(row._mapping) for row in result]

# ✅ 테스트 실행
if __name__ == "__main__":
    test_query = "SELECT TOP 5 * FROM tm_event;"
    print("🔄 SQL 실행 결과:", execute_sql(test_query))
