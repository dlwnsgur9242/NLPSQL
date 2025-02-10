from sqlalchemy import create_engine, MetaData
import urllib
import json

# 데이터베이스 연결 문자열
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-C3BL59A\\SQLEXPRESS;'
    'DATABASE=_dy_solar_5.1_test02;'
    'UID=sa;'
    'PWD=Ydsolemon#@31;'
    'TrustServerCertificate=yes;'
)

# pyodbc 연결 문자열을 URL 인코딩
params = urllib.parse.quote_plus(connection_string)

# SQLAlchemy 엔진 생성
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_url)

# 특정 테이블만 선택하여 메타데이터 가져오기
metadata = MetaData()
selected_tables = {
    "tm_event": ["event_code", "event_desc", "item_code"],
    "th_event": ["event_code", "event_date", "end_date"],
    "tm_user": ["site_name", "kwp", "addr"],
    "tc_device_list": ["item_no", "item_code"],
    "tm_device_item": ["device_code"]
}  # 🎯 필요한 테이블, 컬럼만 선택

metadata.reflect(bind=engine, only=selected_tables.keys())

# 메타데이터 JSON 변환 (컬럼 목록, 기본 키, 외래 키 포함)
database_metadata = {}

for table_name, columns in selected_tables.items():
    table = metadata.tables[table_name]
    table_info = {
        "columns": [column.name for column in table.columns if column.name in columns],
        "primary_key": [key.name for key in table.primary_key.columns] if table.primary_key else [],
        "foreign_keys": []
    }
    
    # 외래 키 정보 추가
    for column in table.columns:
        if column.name in columns:
            for fk in column.foreign_keys:
                table_info["foreign_keys"].append({
                    "column": column.name,
                    "references_table": fk.column.table.name,
                    "references_column": fk.column.name
                })

    database_metadata[table_name] = table_info

# JSON 파일 저장
output_path = "app/data_test/new_metadata.json"
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(database_metadata, json_file, indent=4, ensure_ascii=False)

print(f"✅ MSSQL 메타데이터가 {output_path}에 저장되었습니다.")
