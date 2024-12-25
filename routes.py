from flask import render_template, request, redirect, url_for, session 
from app import app

@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/jobboard')
def jobboard():
    return render_template('jobBoard.html')

@app.route('/technews')
def technews():
    return render_template('Dailytechnews.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/todolist')
def todolist():
    return render_template('todolist.html')

@app.route('/bikesharing')
def bikesharing():
    return render_template('bikesharing.html')

@app.route('/contentsharing')
def contentsharing():
    return render_template('contentsharing.html')