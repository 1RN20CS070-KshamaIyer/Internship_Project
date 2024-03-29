from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import plotly.graph_objects as go


colors = ['#1B1A55', '#9290C3']
req_data = ['Index','P/E','EPS(ttm)','Market Cap'
       ,'Forward P/E','Dividend Est.','Dividend TTM','Debt/Eq','ROI','Gross Margin',
       'Volume','ROE','52W Range','Prev Close','Change']

def load_news(ticker:str):
    fin_url='https://finviz.com/quote.ashx?t='+ticker+'&p=d'
    req=Request(fin_url,headers={'user-agent':'my-app'})
    response=urlopen(req)
    html=BeautifulSoup(response, features="lxml")
    news_table=html.find(id="news-table")
    parsed_data=[]
    for row in news_table.findAll('tr'):
        title=row.a.text
        date_time=row.td.text.replace('\r','').replace('\n','').strip().split(' ')

        if len(date_time) == 1:
            time = date_time[0]
        else:
            date = date_time[0]
    
        parsed_data.append([date,title])
    return parsed_data

def applySentimentAnalysis(news):
    column_headings = ["DATE", "NEWS"]
    df = pd.DataFrame(news, columns=column_headings)

    vader = SentimentIntensityAnalyzer()

    # Calculate sentiment scores for each news item
    df["scores"] = df["NEWS"].apply(lambda text: vader.polarity_scores(text))

    # Extract compound scores for positivity and negativity
    df["compound"] = df["scores"].apply(lambda x: x["compound"])

    # Determine good and bad news based on thresholds (adjust as needed)
    threshold = 0.2
    good_news_count = len(df[df["compound"] > threshold])
    bad_news_count = len(df[df["compound"] < -threshold])

    # Calculate percentages of good and bad news
    total_news = len(df)
    good_news_percentage = round(good_news_count / total_news * 100, 2)
    bad_news_percentage = round(bad_news_count / total_news * 100, 2)

    return good_news_percentage, bad_news_percentage

def drawGraph(good,bad):
    labels = ['Good News', 'Bad News']
    values = [good, bad]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3,marker=dict(colors=colors))])
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(title='Sentiment Analysis Pie Chart', title_x=0.5,width=800)
    return fig.to_json()

def getAdditionalInfo(ticker):
    fin_url='https://finviz.com/quote.ashx?t='+ticker+'&p=d'
    req=Request(fin_url,headers={'user-agent':'my-app'})
    response=urlopen(req)
    html=BeautifulSoup(response,features='lxml')
    add_table=html.find('div',"screener_snapshot-table-wrapper")
    parsed_data={}
    for row in add_table.findAll('tr'):
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        for i in range(0,12,2):
            if row_data[i] in req_data:
                parsed_data[row_data[i]]=row_data[i+1]
    return parsed_data