from flask import render_template
from website import app
import psycopg2
import yfinance as yf
import datetime as dt
from website.TAanalysis import candlesticks, executeIndicator,fib_retrace
from website.FAanalysis import load_news,applySentimentAnalysis,drawGraph,getAdditionalInfo
import talib
from website.pattern import candlestick_patterns

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
async def viewDashboard(ticker):
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM stocks where tickers='{ticker}';'''
    cur.execute(select_query)
    stockData = cur.fetchall()
    cur.close()
    conn.close()

    tickerobj = yf.Ticker(ticker)
    priceData = tickerobj.history(period='1d', start='2023-7-1', end=dt.datetime.today())
    fig = executeIndicator(priceData)

    graph_json = fig.to_json()
    fib = fib_retrace(priceData)
    fib_json=fib.to_json()

    news_data=load_news(ticker)
    pos,neg = applySentimentAnalysis(news_data)
    sentiment_json=drawGraph(pos,neg)

    overview = getAdditionalInfo(ticker)

    return render_template('dashboard.html', graph_json=graph_json,fib_json=fib_json,sentiment_json=sentiment_json,stockName=stockData[0][1], ticker=stockData[0][2],overview=overview)

@app.route('/dashboard/<string:ticker>/news')
def viewNews(ticker):
    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM stocks where tickers='{ticker}';'''
    cur.execute(select_query)
    stockData = cur.fetchall()
    cur.close()
    conn.close()

    news_data=load_news(ticker)
    return render_template('news.html',news_data=news_data,stockName=stockData[0][1], ticker=stockData[0][2])

@app.route('/dashboard/<string:ticker>/screener')
def getScreener(ticker):

    conn = db_conn()
    cur = conn.cursor()

    select_query = f'''SELECT * FROM stocks where tickers='{ticker}';'''
    cur.execute(select_query)
    stockData = cur.fetchall()
    cur.close()
    conn.close()

    pattern_match={}
    tickerobj = yf.Ticker(ticker)
    df = tickerobj.history(period='1d', start='2023-7-1', end=dt.datetime.today())
    for pattern,pattern_name in candlestick_patterns.items():
        pattern_function = getattr(talib,pattern)
        
        results = pattern_function(df['Open'],df['High'],df['Low'],df['Close'])
        last = results.tail(1).values[0]

        if last > 0:
            pattern_match[pattern_name] = 'bullish'
        elif last < 0:
            pattern_match[pattern_name] = 'bearish'

    tickerobj = yf.Ticker(ticker)
    priceData = tickerobj.history(period='1d', start='2023-7-1', end=dt.datetime.today())
    fig = candlesticks(priceData)

    graph_json = fig.to_json()

    return render_template('screener.html',stockName=stockData[0][1], ticker=stockData[0][2],pattern_match=pattern_match, graph_json=graph_json)



