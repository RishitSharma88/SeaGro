from flask import render_template, request, redirect, url_for, session 
from app import app
from models import db, User
from mail import send_reset_email, verify_reset_token
import os
import requests
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
from urllib.parse import urljoin

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = os.getenv('NEWS_API_URL')
COURSE_API_URL = os.getenv('COURSE_API_URL')
JOBS_API_KEY = os.getenv('JOBS_API_KEY')
JOBS_API_URL = os.getenv('JOBS_API_URL')
JOBS_API_HOST_HEADER = os.getenv('JOBS_API_HOST_HEADER')

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            #flash('Please login to continue')
            return redirect(url_for('login'))
    return inner

def fetch_all_courses():

    courses = []
    next_url = COURSE_API_URL  # Start with the base URL
    count = 0

    while next_url and count != 2:
        print(f"Fetching page {count}: {next_url}")
        course_response = requests.get(next_url)

        if course_response.status_code == 200:
            response_data = course_response.json()

            courses.extend(response_data.get('results', []))  # Safely get results
            next_url = response_data.get('pagination', {}).get('next')

            # Handle relative URLs
            if next_url and not next_url.startswith('http'):
                next_url = urljoin(COURSE_API_URL, next_url)

            count += 1
        else:
            print(f"Error: {course_response.status_code}")
            break  # Exit on error

    print(f"Total courses fetched: {len(courses)}")
    return courses

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
    
    session['user_id'] = user.id
    
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
    
    return redirect(url_for('reset_password'))

@app.route('/reset_password')
def reset_password():
    return render_template('resetpassword.html') 

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_post(token):
    #Validate token post method after html page created
    user = verify_reset_token(token)
    if not user:
        #flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))
    new_password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not new_password or new_password != confirm_password:
        #flash('Passwords do not match or are invalid.', 'danger')
        return render_template('resetpassword.html', token=token)
    
    user.password = new_password
    db.session.commit()

    #flash('Your password has been updated. You can now log in.', 'success')
    return redirect(url_for('login'))

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

@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/jobboard')
def jobboard():

    url = JOBS_API_URL
    headers = {
        "x-rapidapi-key": JOBS_API_KEY,
        "x-rapidapi-host": JOBS_API_HOST_HEADER
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jobs = response.json()  
    else:
        jobs = []

    for job in jobs:

        if 'date_posted' in job and job['date_posted']:
            try:
                job['date_posted'] = datetime.strptime(job['date_posted'], "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                job['date_posted'] = "Invalid date"
        else:
            job['date_posted'] = "Date not provided"

        if 'locations_raw' in job and job['locations_raw']:
            location = job['locations_raw'][0]  
            job['address'] = location.get('address', {}).get('addressLocality', '') + ", " + \
                             location.get('address', {}).get('addressCountry', '')
        else:
            job['address'] = "Location not specified"

    return render_template('jobBoard.html', jobs = jobs)

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

@app.route('/learning_course')
def learning_course():
    courses = fetch_all_courses()
    return render_template('learningcourses.html', courses = courses)

@app.route('/learning_course', methods=['POST'])
def learning_course_post():
    query = request.form.get('query', '').lower()
    courses = fetch_all_courses()
    filtered_courses = []

    for course in courses['results']:
        if query in course['name'].lower():
            filtered_courses.append(course)

    return render_template('learningcourses.html', courses = filtered_courses)

@app.route('/community')
@auth_required
def community():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('community.html', user=user)

@app.route('/todolist')
@auth_required
def todolist():
    return render_template('todolist.html')

@app.route('/bike_sharing')
@auth_required
def bike_sharing():
    return render_template('bikesharing.html')

@app.route('/profile')
@auth_required
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
    
@app.route('/profile', methods = ['POST'])
@auth_required
def profile_post():
    id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')

    user = User.query.get(id)

    if not user:
        #flash('Influencer not found')
        return redirect(url_for('login'))
    
    if not username or not email:
        #flash('Fill required fields')
        return redirect(url_for('profile'))
    
    user.username = username
    user.bio = email

    db.session.commit()
    return redirect(url_for('profile'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'] 

@app.route('/upload_profile_pic', methods=['POST'])
@auth_required
def upload_profile_pic():
    if 'profile_pic' not in request.files:
        #flash('No file part')
        return redirect(url_for('profile'))
    
    file = request.files['profile_pic']
    
    if file.filename == '':
        #flash('No selected file')
        return redirect(url_for('profile'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_id = session['user_id']

        new_filename = f"user_{user_id}.{filename.rsplit('.', 1)[1].lower()}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        user = User.query.get(user_id)
        user.profile_pic = new_filename
        db.session.commit()
        
        #flash('Profile picture updated successfully')
        return redirect(url_for('profile'))
    
    #flash('Invalid file format')
    return redirect(url_for('home'))
