from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle
from model import CourseRecommender

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Load the saved model from model.pkl
with open('model.pkl', 'rb') as file:
    recommender = pickle.load(file)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('newcsv.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM data WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['userid'] = user['userid']
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM data WHERE userid = ?', (session['userid'],)).fetchone()
    conn.close()

    if request.method == 'POST':
        goal = request.form.get('goal', '').lower()
        session['goal'] = goal
        return redirect(url_for('courses'))

    return render_template('profile.html', user=user) if user else "User not found."

@app.route('/courses', methods=['GET'])
def courses():
    goal = session.get('goal', None)
    if not goal:
        return redirect(url_for('profile'))

    recommended_courses = recommender.recommend_courses(goal)
    return render_template('courses.html', courses=recommended_courses)

if __name__ == '__main__':
    app.run(debug=True)
