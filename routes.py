from flask import render_template, request, redirect, url_for, session 
from app import app
from models import db, User, Course
from mail import send_reset_email, verify_reset_token
import os
import requests
from werkzeug.utils import secure_filename


NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = os.getenv('NEWS_API_URL')
COURSE_API_URL = os.getenv('COURSE_API_URL')
COURSE_API_KEY = os.getenv('COURSE_API_KEY')
COURSE_API_HOST_HEADER = os.getenv('COURSE_API_HOST_HEADER')

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

    print(fname)
    print(lname)
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

@app.route('/profile')
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
    
@app.route('/profile', methods = ['POST'])
def profile_influencer_post():
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

@app.route('/learning_course')
def learning_course():
    return render_template('learningcourses.html')

@app.route('/learning_course', methods=['POST'])
def learning_course_post():
    query = request.form.get('query', '')  
    max_price = request.form.get('priceRange', 10000)  
    sort_by = request.form.get('sortBy', None)  

    courses = Course.query
    if query:
        courses = courses.filter(Course.title.like(f"%{query}%"))
    if max_price:
        courses = courses.filter(Course.price <= int(max_price))
    if sort_by == 'most_rated':
        courses = courses.order_by(Course.rating.desc())
    elif sort_by == 'newest':
        courses = courses.order_by(Course.id.desc())

    courses = courses.all()

    return render_template('learningcourses.html', courses=courses, query=query, max_price=max_price, sort_by=sort_by)