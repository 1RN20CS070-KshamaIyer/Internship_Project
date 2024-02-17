from flask import render_template,url_for,redirect,request,send_file,jsonify,session
from website import app
import psycopg2
import yfinance as yf
import numpy as np
import datetime as dt
from website.graph import executeIndicator,fib_retrace
from pandas_datareader import data as pdr
from website.FAanalysis import load_news,applySentimentAnalysis,drawGraph


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

@app.route('/dashboard/<string:ticker>')
def viewDashboard(ticker):
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM stocks where tickers='{ticker}';'''
    cur.execute(select_query)
    stockData = cur.fetchall()
    cur.close()
    conn.close()

    tickerobj = yf.Ticker(ticker)
    priceData = tickerobj.history(period='1d', start='2023-7-1', end=dt.datetime.today())
    priceData['Log_Returns'] = np.log(priceData['Close'] / priceData['Close'].shift(1))

    fig = executeIndicator(priceData)

    graph_json = fig.to_json()
    fib = fib_retrace(priceData)
    fib_json=fib.to_json()

    news_data=load_news(ticker)
    pos,neg = applySentimentAnalysis(news_data)
    sentiment_json=drawGraph(pos,neg)

    return render_template('dashboard.html', graph_json=graph_json,fib_json=fib_json,sentiment_json=sentiment_json,stockName=stockData[0][1], ticker=stockData[0][2])
