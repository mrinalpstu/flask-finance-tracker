import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-pro-portfolio'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    expenses = db.relationship('Expense', backref='owner', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
@login_required
def dashboard():
    user_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    
    total_spent = sum(item.amount for item in user_expenses)
    
    # Category wise summary calculation
    category_summary = {}
    for item in user_expenses:
        category_summary[item.category] = category_summary.get(item.category, 0) + item.amount

    return render_template(
        'dashboard.html', 
        expenses=user_expenses, 
        total_spent=total_spent,
        category_summary=category_summary
    )

@app.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')

    if title and amount and category:
        new_expense = Expense(
            title=title,
            amount=float(amount),
            category=category,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete-expense/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
        flash('Item deleted!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/export-csv')
@login_required
def export_csv():
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Amount (USD)', 'Category', 'Date'])
    
    for item in user_expenses:
        writer.writerow([item.id, item.title, item.amount, item.category, item.date.strftime('%Y-%m-%d')])
    
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=expense_report.csv"}
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check if the username is already taken or not
        if User.query.filter_by(username=username).first():
            flash('Username already exists! Choose another.', 'danger')
            return redirect(url_for('register'))

        # Email existence check
        if User.query.filter_by(email=email).first():
            flash('Email already registered! Please login or use a different email.', 'danger')
            return redirect(url_for('register'))

        # If no duplication. create new user
        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and not session.get('_flashes'):
        # কোনো কারণে আগের ক্লিয়ার না হওয়া মেসেজ থাকলে তা মুছে ফেলবে
        pass

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session.pop('_flashes', None)  # সফল লগইনে ফ্ল্যাশ মেসেজ ক্লিয়ার
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)