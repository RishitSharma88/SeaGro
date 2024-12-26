from flask import render_template, request, redirect, url_for, session 
from app import app
from models import db, User
from mail import send_reset_email
import os
import requests

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = os.getenv('NEWS_API_URL')

@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/jobboard')
def jobboard():
    return render_template('jobBoard.html')

@app.route('/tech_news')
def tech_news():
    params = {
        'apikey': NEWS_API_KEY,
        'category': 'technology',
        'lang': 'en',
        'max': 10,
    }

    # Fetch data from News API
    response = requests.get(NEWS_API_URL, params=params)
    news_data = response.json()

    if news_data['totalArticles'] > 0:
        articles = news_data['articles']

    else:
        articles = []

    return render_template('Dailytechnews.html', articles=articles)

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')

@app.route('/bike_sharing')
def bike_sharing():
    return render_template('bikesharing.html')

@app.route('/content_sharing')
def content_sharing():
    return render_template('contentsharing.html')

@app.route('/login')
def login(): 
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post(): 
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        #flash('Please fill out all fields')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        #flash('Username not found')
        return redirect(url_for('login'))
    
    return redirect(url_for('home'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgotpassword.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password_post():
    email = request.form.get('email')

    # Check if the email exists in the database
    user = User.query.filter_by(email=email).first()

    if user:
        send_reset_email(user)
        #flash('A reset link has been sent to your email.', 'success')

    else:
        #flash('Email does not exist.', 'danger')
        return redirect(url_for('forgot_password'))
    
    return redirect(url_for('login'))

@app.route('/reset_password')
def reset_password():
    #Validate token post method after html page created
    return render_template('reset_password') 

@app.route('/create_account')
def create_account():
    return render_template('createaccount.html')

@app.route('/create_account', methods=['POST'])
def create_account_post():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password != confirm_password:
        #flash('Passwords do not match')
        return redirect(url_for('create_account'))
    
    user = User.query.filter_by(username=username).first()

    if user:
        #flash('Username already exists')
        return redirect(url_for('create_account'))
    
    name = fname + " " + lname
    new_user = User(name=name, username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

