from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-key")  # change in production

DATA_FILE = "messages.csv"

def ensure_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","name","email","message"])

ensure_csv()

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/projects')
def projects():
    # Option: you can pass a list of projects to the template to avoid hardcoding.
    projects_list = [
        {"title":"Student Management System", "desc":"Flask + MySQL; CRUD, auth", "img": "images/project1.png"},
        {"title":"Library Management", "desc":"Full-stack web app for college library", "img": "images/project2.png"},
        {"title":"AI Chatbot", "desc":"NLP-based Q&A", "img": "images/project3.png"},
    ]
    return render_template('projects.html', title='Projects', projects=projects_list)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        message = request.form.get('message','').strip()

        if not name or not email or not message:
            flash("Please fill in all fields", "error")
            return redirect(url_for('contact'))

        # append to CSV
        with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.utcnow().isoformat(), name, email, message])

        flash("Thanks — your message has been received!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', title='Contact')

if __name__ == '__main__':
    app.run(debug=True)
