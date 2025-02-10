import json

# JSON 파일 로드
with open("03.project\data_test\ms_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# 메타데이터 요약 생성
summary = {}
for table_name, table_data in metadata.items():
    summary[table_name] = {
        "columns": [col["name"] for col in table_data["columns"]],
        "description": f"{table_name} 테이블에 대한 설명 (추가 가능)",
    }

# 요약 데이터 저장
with open("03.project\data_test\ms_meta_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)

print("요약된 메타데이터가 저장되었습니다.")
