import streamlit as st
import requests

# ✅ FastAPI 서버 주소
API_URL = "http://localhost:8000/convert"

st.title("Text2SQL 변환기 (GPT-4o + MSSQL)")

# ✅ 자연어 질의 입력
query = st.text_input("자연어 질의 입력:")

if st.button("SQL 변환 및 실행"):
    if query:
        # ✅ FastAPI 호출
        response = requests.post(API_URL, json={"query": query})
        result = response.json()
        
        # ✅ SQL 변환 결과 표시
        st.subheader("📌 변환된 SQL:")
        st.code(result["sql"], language="sql")
        
        # ✅ MSSQL 실행 결과 표시
        st.subheader("📊 MSSQL 실행 결과:")
        if result["data"]:
            st.write(result["data"])
        else:
            st.warning("⚠ 데이터가 없습니다.")

        # ✅ 캐싱 여부 표시
        if result["cached"]:
            st.success("✅ 캐싱된 결과를 반환했습니다.")
        else:
            st.info("🔄 새로 생성된 SQL입니다.")
    else:
        st.warning("❗ 질의를 입력하세요.")
