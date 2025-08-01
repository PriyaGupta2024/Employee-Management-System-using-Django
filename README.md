# 🧑‍💼 Employee Management System using Django

A smart and responsive web-based **Employee Management System** built using **Python** and the **Django** framework. 
This application allows you to manage employee data, departments, roles, and admin functionalities from a clean web interface.

---

## 🔧 Tech Stack

- **Backend**: Python 3, Django
- **Frontend**: HTML, CSS (Django Templates)
- **Database**: SQLite (default Django DB)
- **Tools**: VS Code, Git, GitHub

---

## 📁 Project Structure
<pre> <code> office_emp_proj/ ├── emp_app/ # Main Django app │ ├── migrations/ # Database migrations │ ├── static/ # Static files (CSS, JS, images) │ ├── templates/ # HTML templates │ ├── admin.py # Admin panel settings │ ├── models.py # Data models │ ├── urls.py # App-level routes │ └── views.py # Core logic ├── office_emp_proj/ # Django project settings │ ├── settings.py │ └── urls.py # Project routes ├── db.sqlite3 # SQLite database (ignored in .gitignore) ├── manage.py # Django project manager ├── requirements.txt # Python dependencies └── .gitignore # Git ignore file </code> </pre>
## ✨ Features

- ✅ Add, update, delete employee records
- ✅ Assign departments and roles
- ✅ Admin panel for full control
- ✅ Search/filter functionality
- ✅ Django-based structure with reusable components

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/PriyaGupta2024/Employee-Management-System-using-Django.git
   cd Employee-Management-System-using-Django
2. **Create a virtual environment (optional but recommended)**   
   python -m venv env
   source env/bin/activate
   
2. **Install dependencies**
    pip install -r requirements.txt
   
4. **Run migrations**
   python manage.py makemigrations
   python manage.py migrate
   
5. **Start the development server**
    python manage.py runserver
6. **Visit in your browser**
