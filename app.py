# app.py
# This is the main application file.

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import os

# Corrected: Use double underscores for __name__
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# User table model
class User(db.Model):
    # Corrected: Use double underscores for __tablename__
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# This function is deprecated. A better approach is to use Flask-Migrate
# or a manual CLI command to create the database.
# However, for it to work, we need the app context.
with app.app_context():
    db.create_all()

# MODIFIED: This route now renders the home page.
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('signup'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Try logging in.", "warning")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    return render_template('dashboard.html', name=session['user_name'])

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Corrected: Use double underscores for __name__ and __main__
if __name__ == '__main__':
    app.run(debug=True)

# Note: The old db_config dictionary and SECRET_KEY variable have been removed
# because the app now gets all its configuration from the Config class.
