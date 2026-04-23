from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

bp = Blueprint('tasks', __name__)

@bp.route('/')
def index_redirect():
    """首頁重導向至任務列表"""
    return redirect(url_for('tasks.index'))

@bp.route('/tasks')
def index():
    """
    顯示所有任務列表。
    可接受 URL 參數 q (搜尋) 與 status (篩選狀態)。
    渲染: index.html
    """
    tasks = Task.get_all()
    
    # 取得查詢參數
    q = request.args.get('q', '').strip().lower()
    status_filter = request.args.get('status', '')

    # 簡單的在記憶體中進行篩選 (因為 MVP 階段資料量小)
    filtered_tasks = []
    for t in tasks:
        match_q = True
        match_status = True
        
        # 標題或描述包含關鍵字
        if q:
            title_match = q in (t['title'] or '').lower()
            desc_match = q in (t['description'] or '').lower()
            if not (title_match or desc_match):
                match_q = False
            
        # 狀態符合
        if status_filter and t['status'] != status_filter:
            match_status = False
            
        if match_q and match_status:
            filtered_tasks.append(t)

    return render_template('index.html', tasks=filtered_tasks, q=q, status_filter=status_filter)

@bp.route('/tasks/create', methods=['GET', 'POST'])
def create():
    """
    GET: 顯示新增任務表單 (task_form.html)
    POST: 接收表單資料，呼叫 Task.create() 儲存，成功後重導向至任務列表
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()
        category = request.form.get('category', '').strip()
        
        # 驗證必填欄位
        if not title:
            flash('任務標題為必填欄位！', 'danger')
            return render_template('task_form.html', task=request.form)
            
        data = {
            'title': title,
            'description': description if description else None,
            'due_date': due_date if due_date else None,
            'category': category if category else None,
            'status': 'pending'
        }
        
        task_id = Task.create(data)
        if task_id:
            flash('任務新增成功！', 'success')
            return redirect(url_for('tasks.index'))
        else:
            flash('新增任務時發生錯誤，請稍後再試。', 'danger')
            return render_template('task_form.html', task=request.form)
            
    # GET request
    return render_template('task_form.html', task=None)

@bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    GET: 取得指定 id 的任務資料，並顯示編輯表單 (task_form.html)
    POST: 接收編輯表單資料，呼叫 Task.update() 更新資料，成功後重導向至任務列表
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()
        category = request.form.get('category', '').strip()
        status = request.form.get('status', task['status'])
        
        if not title:
            flash('任務標題為必填欄位！', 'danger')
            # 建立一個臨時字典供前端顯示錯誤時保留使用者輸入
            temp_task = dict(task)
            temp_task.update({
                'title': title,
                'description': description,
                'due_date': due_date,
                'category': category,
                'status': status
            })
            return render_template('task_form.html', task=temp_task)
            
        data = {
            'title': title,
            'description': description if description else None,
            'due_date': due_date if due_date else None,
            'category': category if category else None,
            'status': status
        }
        
        if Task.update(id, data):
            flash('任務更新成功！', 'success')
            return redirect(url_for('tasks.index'))
        else:
            flash('更新任務時發生錯誤，請稍後再試。', 'danger')
            return render_template('task_form.html', task=task)

    # GET request
    return render_template('task_form.html', task=task)

@bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    接收 POST 請求以刪除指定任務，呼叫 Task.delete() 後重導向至任務列表
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))
        
    if Task.delete(id):
        flash('任務已成功刪除！', 'success')
    else:
        flash('刪除任務時發生錯誤，請稍後再試。', 'danger')
        
    return redirect(url_for('tasks.index'))

@bp.route('/tasks/<int:id>/status', methods=['POST'])
def update_status(id):
    """
    接收 POST 請求更新指定任務的狀態，呼叫 Task.update() 後重導向至任務列表
    """
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('tasks.index'))
        
    new_status = request.form.get('status')
    valid_statuses = ['pending', 'in_progress', 'completed']
    
    if new_status in valid_statuses:
        if Task.update(id, {'status': new_status}):
            flash('狀態更新成功！', 'success')
        else:
            flash('狀態更新失敗。', 'danger')
    else:
        flash('無效的狀態值。', 'danger')
        
    return redirect(url_for('tasks.index'))
