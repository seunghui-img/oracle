import os
import socket
import oracledb

ORACLE_DATE_FORMAT = os.getenv('ORACLE_DATE_FORMAT', 'YYYY-MM-DD HH24:MI:SS')
ORACLE_BATCH_SIZE = int(os.getenv('ORACLE_BATCH_SIZE', '10000'))
IP_ADDRESS = socket.gethostbyname(socket.gethostname())

# Connect to the database
def connect():
    host = os.getenv('ORACLE_HOST', 'localhost')
    port = int(os.getenv('ORACLE_PORT', '1521'))
    user = os.getenv('ORACLE_APP_USER', 'sample')
    password = os.getenv('ORACLE_APP_USER_PASSWORD', 'cr8qdHgT+WRsB5lmDfBodSGf4haHVT78eIBcTHsHxqg=')
    service_name = os.getenv('ORACLE_SERVICE_NAME', 'XE')
    
    # dsn = f'{user}/{password}@{host}:{port}/{service_name}'
    # connection = oracledb.connect(user=user, password=password, dsn=dsn)
    
    # params = oracledb.ConnectParams(host=host, port=port, service_name=service_name)
    # connection = oracledb.connect(user=user, password=password, params=params)
    
    from service.cryptography import Pay_GetServiceValue
    
    connection = oracledb.connect(
        host=host, 
        port=port, 
        user=user, 
        password=Pay_GetServiceValue(password), 
        service_name=service_name,
    )
    return connection


def select() -> dict:
    with connect() as conn:
        with conn.cursor() as cursor:
            sql = """
            """
            
            # Read a single record
            cursor.execute(statement=sql, parameters=dict(date_fmt=ORACLE_DATE_FORMAT))
            columns = [col[0] for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
            
            record = cursor.fetchone()
    if record:
        return {k.lower() : v for k, v in record.items()}


def select_all(start_dt: str, end_dt: str) -> list[dict]:
    with connect() as conn:
        with conn.cursor() as cursor:
            param = dict()
            param['date_fmt'] = ORACLE_DATE_FORMAT
            
            sql = """
            SELECT  
                    NVL(TO_CHAR(col1, :date_fmt), NULL) AS col1
                    NVL(TO_CHAR(col2, :date_fmt), NULL) AS col2
            FROM    TB_MP_AI_MODEL_META
            WHERE   1=1
            """
            
            if start_dt:
                sql += """
                AND     col1 >= :start_dt
                """
                param['start_dt'] = start_dt
            if end_dt:
                sql += """
                AND     col1 <= :end_dt
                """
                param['end_dt'] = end_dt
            
            sql += """
            ORDER BY 
            """
            
            # Read records
            cursor.execute(statement=sql, parameters=param)
            columns = [col[0] for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
            
            records = cursor.fetchall()
    if records:
        return [{k.lower():v for k,v in i.items()} for i in records]
    return None


def delete(ids: list[int]):
    result = []
    if not ids:
        return
    
    with connect() as conn:
        with conn.cursor() as cursor:
            sql = """
            DELETE FROM 
            RETURNING MODEL_ID INTO :2
            """
            
            # Delete records
            del_rows = cursor.var(str, arraysize=len(ids))
            cursor.setinputsizes(None, del_rows)
            cursor.executemany(statement=sql, parameters=[(id,) for id in ids])
            
            for idx, id in enumerate(ids):
                result += del_rows.getvalue(idx)
        conn.commit()
    return result


def update(obj: object):
    if obj is None:
        return
    
    with connect() as conn:
        with conn.cursor() as cursor:
            sql = """
            UPDATE  
            SET     
            WHERE
            """
            
            # Update a record
            cursor.execute(statement=sql, 
                           parameters=obj.model_dump(exclude=['col1', 'col2']))
            rowcount = cursor.rowcount
        conn.commit()


def insert(obj: object):
    if obj is None:
        return
    
    with connect() as conn:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO  (
                col1, col2, col3
            )
            VALUES (
                :col1, :col2, 1234
            )
            """
            
            # Create a new record
            cursor.execute(statement=sql, 
                           parameters=obj)
            rowcount = cursor.rowcount
        conn.commit()


# csv 파일에서 읽은 데이터 저장
def save_file_data(file_path: str):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.setinputsizes(None, 25)

            with open(file_path, 'r', encoding='utf-8') as csv_file:
                import csv
                csv_reader = csv.reader(csv_file, delimiter='\t')
                next(csv_reader)    # 첫 행 제외
                
                sql = """
                INSERT INTO  (
                    col1, col2, col3, col4
                ) VALUES (
                    :1, :2, :3, SYSDATE
                )
                """
                data = []
                for line in csv_reader:
                    data.append(tuple(line))
                    if len(data) % ORACLE_BATCH_SIZE == 0:
                        cursor.executemany(sql, data)
                        data = []
                if data:
                    cursor.executemany(sql, data)
                conn.commit()
                