import sqlite3
import os

# 確保對應的 instance 目錄存在
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """建立並回傳與 SQLite 資料庫的連線"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓查詢結果可以像字典一樣存取欄位
        return conn
    except sqlite3.Error as e:
        print(f"資料庫連線錯誤: {e}")
        raise

class Task:
    """任務 (Task) 資料庫模型"""

    @staticmethod
    def create(data):
        """
        新增一筆任務記錄
        :param data: dict，包含 title, description, status, due_date, category
        :return: int 新增任務的 id，失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO tasks (title, description, status, due_date, category) 
                VALUES (?, ?, ?, ?, ?)
                ''',
                (
                    data.get('title'),
                    data.get('description'),
                    data.get('status', 'pending'),
                    data.get('due_date'),
                    data.get('category')
                )
            )
            conn.commit()
            task_id = cursor.lastrowid
            return task_id
        except sqlite3.Error as e:
            print(f"新增任務錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有任務記錄，依建立時間反序排列
        :return: list of dict
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            tasks = cursor.fetchall()
            return [dict(task) for task in tasks]
        except sqlite3.Error as e:
            print(f"取得任務列表錯誤: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(task_id):
        """
        取得單筆任務記錄
        :param task_id: 任務 ID
        :return: dict 任務資料，找不到或錯誤時回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            return dict(task) if task else None
        except sqlite3.Error as e:
            print(f"取得單筆任務錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(task_id, data):
        """
        更新指定的任務記錄
        :param task_id: 任務 ID
        :param data: dict，包含欲更新的欄位與新值
        :return: bool 更新是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 取得現有資料
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            if not task:
                return False
                
            new_title = data.get('title', task['title'])
            new_description = data.get('description', task['description'])
            new_status = data.get('status', task['status'])
            new_due_date = data.get('due_date', task['due_date'])
            new_category = data.get('category', task['category'])
            
            cursor.execute(
                '''
                UPDATE tasks 
                SET title = ?, description = ?, status = ?, due_date = ?, category = ? 
                WHERE id = ?
                ''',
                (new_title, new_description, new_status, new_due_date, new_category, task_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"更新任務錯誤: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(task_id):
        """
        刪除指定的任務記錄
        :param task_id: 任務 ID
        :return: bool 刪除是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"刪除任務錯誤: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
