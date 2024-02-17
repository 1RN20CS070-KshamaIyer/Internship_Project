from urllib.request import urlopen,Request
from bs4 import BeautifulSoup

def load_news(ticker:str):
    fin_url='https://finviz.com/quote.ashx?t='+ticker+'&p=d'
    req=Request(fin_url,headers={'user-agent':'my-app'})
    response=urlopen(req)
    html=BeautifulSoup(response, 'html')
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