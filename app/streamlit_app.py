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
        
        # 🔍 디버깅 코드 추가
        print("📡 HTTP 상태 코드:", response.status_code)
        print("📡 응답 본문:", response.text[:500])  # 응답 일부 출력
        
        try:
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
        except requests.exceptions.JSONDecodeError:
            st.error("❌ JSON 파싱 오류: 서버 응답이 JSON 형식이 아닙니다.")
            print("❌ JSONDecodeError 발생 - 응답이 JSON이 아님!")
    else:
        st.warning("❗ 질의를 입력하세요.")
