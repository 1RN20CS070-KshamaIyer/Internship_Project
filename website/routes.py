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

@app.route('/dashboard/<string:ticker>', methods=['GET'])
def viewDashboard(ticker):
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM stocks where tickers='{ticker}';'''
    cur.execute(select_query)
    stockData = cur.fetchall()
    print(stockData)

    # Getting the historical data for the ticker
    tickerobj = yf.Ticker(ticker)
    priceData = tickerobj.history(period='1d', start='2024-1-1', end=dt.datetime.today())
    priceData['Log_Returns'] = np.log(priceData['Close'] / priceData['Close'].shift(1))

    # Generate graphs for all indicators
    graph_json_dict = {}
    for indicator in ['SMA', 'ATR', 'Stochastic', 'MACD', 'Bollinger bands', 'rate of change', 'RSI', 'Fibonnaci Retracement']:
        graph_json_dict[indicator] = executeIndicator(indicator, priceData)

    return render_template('dashboard.html', stockName=stockData[0][1], ticker=stockData[0][2], graph_json_dict=graph_json_dict)
