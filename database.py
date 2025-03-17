import psycopg2, os
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

class Database():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get('DB_HOST'),
                dbname=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                port=os.environ.get('DB_PORT')
            )
            self.cursor = self.conn.cursor()
            
            # 테이블 생성
            self.create_tables()
        except Error as e:
            print(f"데이터베이스 연결 실패: {e}")

    def create_tables(self):
        try:
            # schedules 테이블 생성
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS schedules (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    date DATE NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
        except Error as e:
            print(f"테이블 생성 실패: {e}")

    def add_schedule(self, user_id: int, date: str, content: str) -> bool:
        try:
            sql = """
                INSERT INTO schedules (user_id, date, content)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(sql, (user_id, date, content))
            self.conn.commit()
            return True
        except Error as e:
            print(f"일정 추가 실패: {e}")
            return False

    def get_schedules(self, user_id: int) -> list:
        try:
            sql = """
                SELECT id, date, content 
                FROM schedules 
                WHERE user_id = %s 
                ORDER BY date
            """
            self.cursor.execute(sql, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"일정 조회 실패: {e}")
            return []

    def delete_schedule(self, schedule_id: int, user_id: int) -> bool:
        try:
            sql = """
                DELETE FROM schedules 
                WHERE id = %s AND user_id = %s
            """
            self.cursor.execute(sql, (schedule_id, user_id))
            deleted = self.cursor.rowcount > 0
            self.conn.commit()
            return deleted
        except Error as e:
            print(f"일정 삭제 실패: {e}")
            return False

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

class CRUD(Database):

    def create(self, schema, table, colum, data):
        sql = " INSERT INTO {schema}.{table}({colum}) VALUES ('{data}') ;".format(schema=schema,table=table,colum=colum,data=data)
        try:
            self.cursor.execute(sql)
            self.conn.commit()       
        except Exception as e:
            print("insert DB",e)

    def get(self, schema, table, colum):
        sql = " SELECT {colum} form {schema}. {table}".format(colum=colum, schema=schema, table=table)
        try:
            self.cursor.execute(sql)
            # get 요청 commit X
            result = self.cursor.fetchall()
        except Exception as e:
            result = (" get err",e)
        return result

    def update(self, schema, table, colum, value, condition):
        sql = " UPDATE {schema}.{table} SET {colum}='{value}' WHERE {colum}='{condition}' ".format(schema=schema, table=table , colum=colum ,value=value,condition=condition )
        try :
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e :
            print(" update DB err",e)

    def delete(self, schema, table, condition):
        sql = " delete from {schema}.{table} where {condition} ; ".format(schema=schema,table=table, condition=condition)
        try :
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print( "delete DB err", e)