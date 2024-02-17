from flask import render_template,url_for,redirect,request,send_file,jsonify,session
from website import app
import psycopg2
import yfinance as yf
import numpy as np
import datetime as dt
from website.TAanalysis import executeIndicator
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

@app.route('/dashboard/<string:ticker>', methods=['GET', 'POST'])
def viewDashboard(ticker):
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM stocks where tickers='{ticker}';'''
    cur.execute(select_query)
    stockData = cur.fetchall()

    tickerobj = yf.Ticker(ticker)
    priceData = tickerobj.history(period='1d', start='2024-1-1', end=dt.datetime.today())
    priceData['Log_Returns'] = np.log(priceData['Close'] / priceData['Close'].shift(1))

    if request.method == 'POST':
        indicator = request.form['option']
        session['selected_indicator'] = indicator  # Store the selected indicator in the session
        graph_json1 = executeIndicator(indicator, priceData)
        return render_template('dashboard.html', stockName=stockData[0][1], ticker=stockData[0][2], graph_json=graph_json1)
    
    # Check if there's a selected indicator in the session, if not, default to 'ATR'
    selected_indicator = session.get('selected_indicator', 'SMA')
    graph_json = executeIndicator(selected_indicator, priceData)

    return render_template('dashboard.html', stockName=stockData[0][1], ticker=stockData[0][2], graph_json=graph_json)