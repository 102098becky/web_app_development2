import os
import sqlite3
from flask import Flask
from app.routes.task_routes import bp as task_bp

def create_app():
    app = Flask('app')
    
    # 載入環境變數或使用預設值
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 確保 instance 資料夾存在，用於存放 database.db
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 註冊 Blueprints
    app.register_blueprint(task_bp)
    
    # 初始化資料庫
    init_db()
    
    return app

def init_db():
    """初始化資料庫的輔助函式"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    if os.path.exists(schema_path):
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
        print("資料庫初始化完成！")
    else:
        print(f"找不到 schema 檔案: {schema_path}")

app = create_app()

if __name__ == '__main__':
    # 若直接執行此檔案，則啟動開發伺服器
    app.run(debug=True)
