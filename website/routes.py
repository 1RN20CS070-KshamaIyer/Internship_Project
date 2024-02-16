from flask import render_template,url_for,redirect,request,send_file,jsonify
from website import app
import psycopg2

def db_conn():
    conn = psycopg2.connect(database="mydatabase", host="localhost", user="myuser",password="mypassword",port="5432")
    return conn

@app.route('/')
def home():
    conn=db_conn()
    cur=conn.cursor()
    select_query = f'''SELECT stockname,tickers FROM stocks;'''
    cur.execute(select_query)
    data = cur.fetchall()

    return render_template('home.html',data=data)