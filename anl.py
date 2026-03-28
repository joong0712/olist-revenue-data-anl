import kagglehub, os, pandas as pd
from sqlalchemy import create_engine

# --- [1단계] 데이터 다운로드 및 경로 설정 ---
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

# --- [2단계] DB 연결 고리 만들기 (트럭 준비) ---
# 구조: "db종류+드라이버://ID:PW@주소:포트/DB이름"
engine = create_engine("mysql+pymysql://root:root@localhost:3306/ecommerce")

# --- [3단계] 반복문으로 모든 CSV 밀어넣기 ---
for file in os.listdir(path):
    if file.endswith(".csv"):
        # 파일명에서 .csv 떼고 테이블 이름 정하기
        table_name = file.replace(".csv", "")
        
        # 읽기 (Pandas)
        df = pd.read_csv(os.path.join(path, file))
        
        # 쓰기 (SQL) - if_exists='replace'는 '기존꺼 지우고 새로 만들기'
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        print(f"Table [{table_name}] 저장 완료!")