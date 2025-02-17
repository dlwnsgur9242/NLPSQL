import openai
import os
import json
import re
from config import OPENAI_API_KEY, GPT_MODEL
from metadata_loader import load_metadata

# ✅ MSSQL 메타데이터 로드
metadata = load_metadata()

openai.api_key = OPENAI_API_KEY

def gpt_text_to_sql(query):
    """GPT-4o를 사용하여 자연어 질의를 SQL로 변환"""
    
    prompt = f"""
    You are an AI assistant that converts natural language questions into SQL queries.
    Based on the following database metadata, generate an optimized SQL query:

    Database Metadata:
    {json.dumps(metadata, indent=2, ensure_ascii=False)}

    User Query: "{query}"

    SQL Query:
    """
# 수정중
    response = openai.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a SQL expert that generates highly optimized queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql_query = response.choices[0].message.content

    # # 🔥 백틱 자동 제거
    sql_query = re.sub(r"```[sS]*?sql|```", "", sql_query, flags=re.IGNORECASE).strip()

    if not sql_query.endswith(";"):
        sql_query += ";"

    return sql_query

# ✅ 테스트 실행
if __name__ == "__main__":
    query = "2023년 4월부터 6월까지 과전압 발생한 발전소만 보여줘"
    print("🔥 GPT-4o 변환 SQL 결과:", gpt_text_to_sql(query))
