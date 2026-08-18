# 💰 Smart Expense Tracker & Financial Dashboard (Flask)

A full-stack Python Flask web application designed for personal expense tracking, budgeting, and CSV data export.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Database](https://img.shields.io/badge/Database-SQLite%2FSQLAlchemy-orange)

## 🌟 Key Features
- **Authentication & Security:** Secure Signup & Login system using `Flask-Login` and `Werkzeug` scrypt password hashing.
- **Relational Database:** One-to-Many relationship between Users and Expenses using `Flask-SQLAlchemy`.
- **Financial Analytics:** Dynamic category-wise summary and total spending breakdown.
- **Data Export:** Export user expense records instantly to CSV format.
- **Responsive UI:** Built with Bootstrap 5 for seamless mobile and desktop experience.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend:** HTML5, Jinja2 Templates, Bootstrap 5
- **Database:** SQLite (Relational ORM)

## Live Demo

https://flask-finance-tracker-j8ny.onrender.com/login?next=%2F

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mrinalpstu/flask-finance-tracker.git]
   cd flask-finance-tracker