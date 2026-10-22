# 📝 TaskFlow - Django To-Do List Application

A modern, full-featured To-Do List web application built with **Django** and **Bootstrap 5**. Designed with complete user authentication, user task isolation, interactive task completion toggling, priority levels, due date tracking, and search/filtering capabilities.

---

## 🌟 Key Features

- 🔐 **User Authentication & Authorization**:
  - Secure registration, login, and logout.
  - Strict user data isolation: each user can only see, create, edit, or delete their own tasks.
  - Unauthenticated visitors are automatically redirected to the login page.
- ➕ **Add Tasks**:
  - Title, description, due date, and priority (High, Medium, Low).
- ✏️ **Edit Tasks**:
  - Update title, description, priority, due date, or toggle completion.
- 🗑️ **Delete Tasks**:
  - Dedicated confirmation screen to prevent accidental deletions.
- ✅ **One-Click Toggle Completion**:
  - Mark tasks complete or incomplete instantly with intuitive visual feedback (checkmarks & strikethroughs).
- 🔍 **Search & Filters**:
  - Search tasks by keyword in title or description.
  - Filter tasks by status: *All*, *Active / Pending*, or *Completed*.
  - Filter tasks by priority: *High*, *Medium*, or *Low*.
- 📊 **Progress Dashboard**:
  - Visual progress bar and counters for total, completed, and pending tasks.
- 📅 **Deadlines & Overdue Indicators**:
  - Automatically flags tasks that are overdue or due today with warning badges.
- 🛡️ **Django Admin Integration**:
  - Full admin management dashboard configured with search and filters.

---

## 📁 Project Structure

```text
django_todo_app/
├── manage.py
├── requirements.txt
├── README.md
├── static/
│   └── css/
│       └── styles.css
├── todo_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── todos/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   └── 0001_initial.py
    └── templates/
        └── todos/
            ├── base.html
            ├── login.html
            ├── register.html
            ├── task_confirm_delete.html
            ├── task_form.html
            └── task_list.html
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Pip package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. (Optional) Create an Admin Superuser
```bash
python manage.py createsuperuser
```
Follow the interactive prompts to set your admin username, email, and password.

### 5. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

---

## 🧪 Running Automated Tests

Run the test suite covering authentication, permissions, CRUD operations, and filtering:

```bash
python manage.py test
```

---

## 🔑 Default URLs

| Route | Description |
|---|---|
| `/` | Main Task Dashboard (requires login) |
| `/task/new/` | Create a new task |
| `/task/<id>/edit/` | Edit an existing task |
| `/task/<id>/delete/` | Delete an existing task (with confirmation) |
| `/task/<id>/toggle/` | Quick toggle between completed and incomplete |
| `/login/` | User login page |
| `/register/` | User registration / sign up page |
| `/logout/` | User logout endpoint |
| `/admin/` | Django Administration panel |
