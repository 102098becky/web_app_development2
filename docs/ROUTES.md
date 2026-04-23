# 任務管理系統 - 路由設計 (Routes Design)

本文件定義系統所有的 URL 路由，並描述對應的 HTTP 方法、處理邏輯與 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁重導向 | GET | `/` | — | 自動重導向至 `/tasks` |
| 任務列表 | GET | `/tasks` | `index.html` | 顯示所有任務，支援搜尋與狀態篩選 |
| 新增任務頁面 | GET | `/tasks/create` | `task_form.html` | 顯示空白任務新增表單 |
| 建立任務 | POST | `/tasks/create` | — | 接收表單並寫入資料庫，成功後重導向列表 |
| 編輯任務頁面 | GET | `/tasks/<int:id>/edit`| `task_form.html` | 顯示帶有原資料的表單 |
| 更新任務 | POST | `/tasks/<int:id>/edit`| — | 接收編輯表單並更新資料庫，重導向列表 |
| 刪除任務 | POST | `/tasks/<int:id>/delete`| — | 刪除指定任務，重導向列表 |
| 更新狀態 | POST | `/tasks/<int:id>/status`| — | 改變任務的完成/未完成狀態，重導向列表 |

## 2. 每個路由的詳細說明

### 首頁重導向
- **URL**：`GET /`
- **處理邏輯**：使用 `redirect` 將使用者導向 `/tasks`。

### 任務列表
- **URL**：`GET /tasks`
- **輸入**：URL 參數 `status` (篩選狀態)、`q` (搜尋關鍵字)。
- **處理邏輯**：呼叫 `Task.get_all()` 並根據參數篩選結果。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：無特定錯誤，若無資料則顯示空列表提示。

### 新增任務頁面
- **URL**：`GET /tasks/create`
- **輸入**：無。
- **處理邏輯**：準備渲染空白表單。
- **輸出**：渲染 `task_form.html`。

### 建立任務
- **URL**：`POST /tasks/create`
- **輸入**：表單欄位 `title`, `description`, `due_date`, `category`。
- **處理邏輯**：驗證 `title` 是否為空。呼叫 `Task.create(...)` 存入 DB。
- **輸出**：重導向至 `/tasks`。
- **錯誤處理**：若 `title` 缺失，返回表單並顯示錯誤訊息。

### 編輯任務頁面
- **URL**：`GET /tasks/<int:id>/edit`
- **輸入**：路徑變數 `id`。
- **處理邏輯**：呼叫 `Task.get_by_id(id)` 取得該筆資料。
- **輸出**：渲染 `task_form.html`，並將 task 資料傳入模板。
- **錯誤處理**：若找不到該 id，返回 404 頁面或重導向並顯示「任務不存在」。

### 更新任務
- **URL**：`POST /tasks/<int:id>/edit`
- **輸入**：路徑變數 `id`，表單欄位 `title`, `description`, `status`, `due_date`, `category`。
- **處理邏輯**：驗證 `title`。呼叫 `Task.update(id, ...)`。
- **輸出**：重導向至 `/tasks`。
- **錯誤處理**：找不到任務回傳 404；`title` 缺失返回表單顯示錯誤。

### 刪除任務
- **URL**：`POST /tasks/<int:id>/delete`
- **輸入**：路徑變數 `id`。
- **處理邏輯**：呼叫 `Task.delete(id)`。
- **輸出**：重導向至 `/tasks`。
- **錯誤處理**：找不到任務回傳 404。

### 更新狀態
- **URL**：`POST /tasks/<int:id>/status`
- **輸入**：路徑變數 `id`，表單欄位傳遞新的 `status`。
- **處理邏輯**：呼叫 `Task.update(id, status=new_status)`。
- **輸出**：重導向至 `/tasks`。
- **錯誤處理**：找不到任務回傳 404。

## 3. Jinja2 模板清單

所有的模板將存放在 `app/templates/` 中。

1. **`base.html`**
   - 包含共通的 `<html>` 結構、標頭 (`<head>`)、CSS 引入與導覽列。
   - 提供 `{% block content %}{% endblock %}` 供子模板繼承。
2. **`index.html`**
   - 繼承 `base.html`。
   - 包含搜尋框、狀態篩選按鈕與任務列表清單。
3. **`task_form.html`**
   - 繼承 `base.html`。
   - 共用於「新增」與「編輯」任務，會根據傳入的 `task` 變數來決定是空白表單還是填入既有資料。

## 4. 路由骨架程式碼

路由的骨架程式碼已建立於 `app/routes/task_routes.py`，使用 Flask Blueprint 來組織路由，目前僅包含函式定義與 docstring，實作將於後續階段補齊。
