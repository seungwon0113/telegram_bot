import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='schedule.db'):
        self.db_name = db_name
        self.init_db()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS schedules
                (id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 date DATE,
                 content TEXT,
                 created_at TIMESTAMP)
            ''')
    
    def add_schedule(self, user_id: int, date: str, content: str) -> bool:
        try:
            with self._get_connection() as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO schedules (user_id, date, content, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, date, content, datetime.now()))
                return True
        except Exception as e:
            print(f"Error adding schedule: {e}")
            return False
    
    def get_schedules(self, user_id: int) -> list:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            SELECT id, date, content FROM schedules
            WHERE user_id = ?
            ORDER BY date
        ''', (user_id,))
        schedules = c.fetchall()
        conn.close()
        return schedules
    
    def delete_schedule(self, schedule_id: int, user_id: int) -> bool:
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''
                DELETE FROM schedules
                WHERE id = ? AND user_id = ?
            ''', (schedule_id, user_id))
            success = c.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except Exception as e:
            print(f"Error deleting schedule: {e}")
            return False
