from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

# 建立 Blueprint，將所有的路由加上任務前綴以便管理 (這裡選擇掛在根目錄，但可以透過註冊時決定)
bp = Blueprint('tasks', __name__)

@bp.route('/')
def index_redirect():
    """首頁重導向至任務列表"""
    pass

@bp.route('/tasks')
def index():
    """
    顯示所有任務列表。
    可接受 URL 參數 q (搜尋) 與 status (篩選狀態)。
    渲染: index.html
    """
    pass

@bp.route('/tasks/create', methods=['GET', 'POST'])
def create():
    """
    GET: 顯示新增任務表單 (task_form.html)
    POST: 接收表單資料，呼叫 Task.create() 儲存，成功後重導向至任務列表
    """
    pass

@bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    GET: 取得指定 id 的任務資料，並顯示編輯表單 (task_form.html)
    POST: 接收編輯表單資料，呼叫 Task.update() 更新資料，成功後重導向至任務列表
    """
    pass

@bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    接收 POST 請求以刪除指定任務，呼叫 Task.delete() 後重導向至任務列表
    """
    pass

@bp.route('/tasks/<int:id>/status', methods=['POST'])
def update_status(id):
    """
    接收 POST 請求更新指定任務的狀態，呼叫 Task.update() 後重導向至任務列表
    """
    pass
