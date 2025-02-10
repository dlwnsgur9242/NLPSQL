import json

# 📂 기존 메타데이터 JSON 파일 로드
input_file = "app\data_test\\new_metadata.json"
output_file = "app\data_test\\new_metadata_updated.json"

with open(input_file, "r", encoding="utf-8") as f:
    metadata = json.load(f)
# 📌 테이블 설명 추가 (AI가 SQL 생성 시 이해하기 쉽게)
table_descriptions = {
    "tm_event": "이벤트 정보",
    "th_event": "이벤트 1분 히스토리",
    "tm_user": "사용자 정보",
    "tc_device_list": "장비 목록",
    "tm_device_item": "장비 정보"
}

# 📌 컬럼별 기본 설명 추가 (AI가 SQL 생성 시 이해하기 쉽게)
column_descriptions = {
    "sl_id": "사이트 번호",
    "item_code": "장비 코드",
    "event_code": "이벤트 코드",
    "event_desc": "이벤트 설명",
    "event_date": "이벤트 발생 시간",
    "end_date": "이벤트 종료 시간",
    "site_name": "사이트 이름",
    "addr": "주소",
    "kwp": "수용 가능한 용량",
    "item_no": "장비 등록 번호",
    "item_code": "장비 코드",
    "device_code": "장비 식별코드"
    # "item_code": "장비 코드",
    # "event_code": "이벤트 코드 (발생한 이벤트의 고유 코드)",
    # "event_desc": "이벤트 명",
    # "event_type": "이벤트 타입",
    # "confirm_flag": "이벤트 확인 여부 (true=확인됨, false=미확인)",
    # "event_date": "이벤트 발생 시간",
    # "confirm_date": "이벤트 확인 시간",
    # "u_id": "접속 ID",
    # "site_name": "사이트 이름",
    # "ip_addr": "IP 주소",
    # "url_addr": "URl 주소"
}

# 📌 기존 구조를 유지하면서 컬럼에 설명 추가
for table_name, table_data in metadata.items():
    # 테이블 설명 추가
    table_data["description"] = table_descriptions.get(table_name, "설명 추가 필요")

    # 컬럼 설명 추가
    updated_columns = []
    for column_name in table_data["columns"]:
        updated_columns.append({
            "name": column_name,
            "description": column_descriptions.get(column_name, "설명 추가 필요")  # 기본 설명 추가
        })
    table_data["columns"] = updated_columns

# 📂 새 JSON 파일로 저장
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

print(f"✅ 컬럼 설명이 추가된 JSON이 {output_file}에 저장되었습니다!")
