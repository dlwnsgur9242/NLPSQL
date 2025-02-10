import json

# ✅ MSSQL 메타데이터 로드 함수
def load_metadata():
    with open("..\\data\\new_metadata_updated.json", "r", encoding="utf-8") as file:
        metadata = json.load(file)
    return metadata

# ✅ 테스트 실행
if __name__ == "__main__":
    metadata = load_metadata()
    print("📌 데이터베이스 테이블 목록:", list(metadata.keys()))
