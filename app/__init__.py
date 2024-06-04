import os
import sys
import platform
import oracledb
import time

app_home = os.path.abspath(os.path.dirname(__file__))
project_home = os.path.dirname(app_home)

os.environ['PROJECT_HOME'] = project_home
os.environ['APP_HOME'] = app_home

sys.path.append(app_home)

# 클라이언트 라이브러리 압축 해제
ORACLE_CLIENT_PATH = os.getenv('ORACLE_CLIENT_PATH', '')

if not os.path.exists(ORACLE_CLIENT_PATH) or (os.path.exists(ORACLE_CLIENT_PATH) and len(os.listdir(ORACLE_CLIENT_PATH)) == 0):
    zip_path = ''
    
    if platform.system() == "Linux" and 'instantclient-basic-linux.x64-11.2.0.4.0.zip' in os.listdir(project_home):
        zip_path = os.path.join(project_home, 'instantclient-basic-linux.x64-11.2.0.4.0.zip')
        
    if platform.system() == "Windows" and 'instantclient-basic-windows.x64-11.2.0.4.0.zip' in os.listdir(project_home):
        zip_path = os.path.join(project_home, 'instantclient-basic-windows.x64-11.2.0.4.0.zip')

    if os.path.exists(zip_path):
        import zipfile
        zip_file = zipfile.ZipFile(zip_path)
        zip_file.extractall(path=os.path.abspath(os.path.dirname(ORACLE_CLIENT_PATH)))
        time.sleep(3)


# Thick 모드 (오라클 DBMS 통신)
if platform.system() == "Windows":
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
else:
    # 리눅스의 경우, 파이썬 환경변수 설정으로 연결 불가
    # 서버 시작 전, 환경 변수 추가할 것
    # export PATH=$PATH:~/instantclient_11_2
    # export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/instantclient_11_2
    oracledb.init_oracle_client()