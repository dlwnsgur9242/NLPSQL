import pyodbc

def test_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=127.0.0.1,35791;'
            'DATABASE=_dy_solar_5.1;'
            'UID=sa;'
            'PWD=Ydsolemon#@31;'
            'TrustServerCertificate=yes;'
        )
        print("데이터베이스 연결 성공!")
        conn.close()
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")

if __name__ == "__main__":
    test_db_connection()