from fastapi import FastAPI
from pydantic import BaseModel
import openai
from sqlalchemy import text
from cache_manager import get_sql_from_cache, store_sql_to_cache
from gpt_text2sql import gpt_text_to_sql
from db_manager import execute_sql, engine
from config import OPENAI_API_KEY, GPT_MODEL
import uvicorn

app = FastAPI()

openai.api_key = OPENAI_API_KEY
print("🔑 OpenAI API Key:", openai.api_key)
print("🔑 OpenAI API Key:", OPENAI_API_KEY)

# ✅ 요청 데이터 모델 정의
class QueryRequest(BaseModel):
    query: str

@app.get("/status")
async def check_status():
    """✅ GPT API 및 MSSQL DB 연결 상태 확인"""
    status = {"gpt_api": False, "db_connection": False}

    # ✅ GPT API 테스트
    try:
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "system", "content": "Test connection"}],
        )
        response = response.choices[0].message.content
        if response:
            status["gpt_api"] = True
    except Exception as e:
        status["gpt_api_error"] = str(e)

    # ✅ MSSQL DB 연결 테스트
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result:
                status["db_connection"] = True
    except Exception as e:
        status["db_error"] = str(e)

    return status

@app.post("/convert")
async def convert_text_to_sql(request: QueryRequest):
    """자연어 질의를 SQL로 변환하는 API"""

    query = request.query

    # ✅ 캐싱된 SQL이 있으면 반환
    cached_sql = get_sql_from_cache(query)
    if cached_sql:
        return {"sql": cached_sql, "cached": True}

    # ✅ GPT-4o 호출하여 변환
    sql_query = gpt_text_to_sql(query)

    # ✅ 변환된 SQL을 캐싱
    store_sql_to_cache(query, sql_query)

    # ✅ MSSQL에서 SQL 실행 후 데이터 반환
    result = execute_sql(sql_query)

    return {"sql": sql_query, "cached": False, "data": result}

@app.get("/cache")
async def get_cached_queries():
    """현재 캐싱된 SQL 목록 확인"""
    return {"message": "Caching is enabled but direct cache listing is not implemented yet."}

# ✅ FastAPI 서버 실행 (로컬에서 실행하려면: `uvicorn fastapi_server:app --reload`)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)