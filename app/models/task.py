import sqlite3
import os

# 確保對應的 instance 目錄存在
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """建立並回傳與 SQLite 資料庫的連線"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以像字典一樣存取
    return conn

class Task:
    @staticmethod
    def create(title, description=None, status='pending', due_date=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO tasks (title, description, status, due_date, category) 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (title, description, status, due_date, category)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = cursor.fetchall()
        conn.close()
        return [dict(task) for task in tasks]

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()
        return dict(task) if task else None

    @staticmethod
    def update(task_id, title=None, description=None, status=None, due_date=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 取得現有資料
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        if not task:
            conn.close()
            return False
            
        new_title = title if title is not None else task['title']
        new_description = description if description is not None else task['description']
        new_status = status if status is not None else task['status']
        new_due_date = due_date if due_date is not None else task['due_date']
        new_category = category if category is not None else task['category']
        
        cursor.execute(
            '''
            UPDATE tasks 
            SET title = ?, description = ?, status = ?, due_date = ?, category = ? 
            WHERE id = ?
            ''',
            (new_title, new_description, new_status, new_due_date, new_category, task_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        return True
