# from flask import render_template,url_for,redirect,request,send_file,jsonify
from website import app

@app.route('/')
def home():
    return 'hello'