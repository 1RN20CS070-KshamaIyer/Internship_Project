import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

def executeIndicator(indicator,data):

    if indicator=='SMA':
        fig=call_SMA(data)
        return fig
    elif indicator=='ATR':
        fig=call_ATR(data)
        return fig
    elif indicator=='Stochastic':
        fig=call_stochastic(data)
        return fig
    elif indicator=='MACD':
        fig=call_macd(data)
        return fig
    elif indicator=='Bollinger bands':
        fig=call_bollinger(data)
        return fig
    elif indicator=='rate of change':
        fig=call_rac(data)
        return fig
    elif indicator=='RSI':
        fig=call_rsi(data)
        return fig
    elif indicator=='Fibonnaci Retracement':
        fig=fib_retrace(data)
        return fig

def call_SMA(data):
    data['SMA_5']=data['Close'].rolling(window=5).mean()
    data['SMA_20']=data['Close'].rolling(window=20).mean()
    data['SMA_ratio']=data['SMA_20']/data['SMA_5']

    fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_5'], mode='lines', name='SMA 5'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], mode='lines', name='SMA 20'))
    return fig

def atr(high, low, close, n=14):
    tr = np.amax(np.vstack(((high - low).to_numpy(), (abs(high - close)).to_numpy(), (abs(low - close)).to_numpy())).T, axis=1)
    return pd.Series(tr).rolling(n).mean().to_numpy()

def call_ATR(data):
    data['ATR']=atr(data['High'], data['Low'], data['Close'], 20)

    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    atr_trace = go.Scatter(x=data.index, y=data['ATR'], mode='lines', name='ATR')

    # Create subplots
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(atr_trace, row=2, col=1)

    # Update layout for better visualization
    fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

def call_stochastic(data):
    data['Lowest_5D'] = data['Low'].rolling(window = 5).min()
    data['High_5D'] = data['High'].rolling(window = 5).max()
    data['Lowest_15D'] = data['Low'].rolling(window = 15).min()
    data['High_15D'] = data['High'].rolling(window = 15).max()

    data['Stochastic_5'] = ((data['Close'] - data['Lowest_5D'])/(data['High_5D'] - data['Lowest_5D']))*100
    data['Stochastic_15'] = ((data['Close'] - data['Lowest_15D'])/(data['High_15D'] - data['Lowest_15D']))*100

    data['Stochastic_%D_5'] = data['Stochastic_5'].rolling(window = 5).mean()
    data['Stochastic_%D_15'] = data['Stochastic_5'].rolling(window = 15).mean()

    data['Stochastic_Ratio'] = data['Stochastic_%D_5']/data['Stochastic_%D_15']

    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    stoch_trace1 = go.Scatter(x=data.index, y=data['Stochastic_%D_5'], mode='lines', name='Stochastic_%D_5')
    stoch_trace2 = go.Scatter(x=data.index, y=data['Stochastic_%D_15'], mode='lines', name='Stochastic_%D_15')

    # Create subplots
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(stoch_trace1, row=2, col=1)
    fig.add_trace(stoch_trace2, row=2, col=1)

    # Update layout for better visualization
    fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

def call_macd(data):
    data['5Ewm'] = data['Close'].ewm(span=5, adjust=False).mean()
    data['15Ewm'] = data['Close'].ewm(span=15, adjust=False).mean()
    data['MACD'] = data['15Ewm'] - data['5Ewm']

    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    macd_trace = go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='ATR')

    # Create subplots
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(macd_trace, row=2, col=1)

    # Update layout for better visualization
    fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

def call_bollinger(data):
    data['15MA'] = data['Close'].rolling(window=15).mean()
    data['SD'] = data['Close'].rolling(window=15).std()
    data['upperband'] = data['15MA'] + 2*data['SD']
    data['lowerband'] = data['15MA'] - 2*data['SD']
    
    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    bollinger_trace1 = go.Scatter(x=data.index, y=data['upperband'], mode='lines', name='Upperband')
    bollinger_trace2 = go.Scatter(x=data.index, y=data['lowerband'], mode='lines', name='Lowerband')
    bollinger_trace3 = go.Scatter(x=data.index, y=data['15MA'], mode='lines', name='SMA_15')

    # Create subplots
    main_fig.add_trace(bollinger_trace1)
    main_fig.add_trace(bollinger_trace2)
    main_fig.add_trace(bollinger_trace3)

    # Update layout for better visualization
    main_fig.update_layout(xaxis_rangeslider_visible=True)
    return main_fig

def call_rac(data):
    data['RC'] = data['Close'].pct_change(periods = 20)

    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    racd_trace = go.Scatter(x=data.index, y=data['RC'], mode='lines', name='RC')

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(racd_trace, row=2, col=1)

    # Update layout for better visualization
    fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

def call_rsi(data):
    data['Diff'] = data['Close'].transform(lambda x: x.diff())
    data['Up'] = data['Diff']
    data.loc[(data['Up']<0), 'Up'] = 0

    data['Down'] = data['Diff']
    data.loc[(data['Down']>0), 'Down'] = 0 
    data['Down'] = abs(data['Down'])

    data['avg_5up'] = data['Up'].rolling(window=5).mean()
    data['avg_5down'] = data['Down'].rolling(window=5).mean()

    data['avg_15up'] = data['Up'].rolling(window=15).mean()
    data['avg_15down'] = data['Down'].rolling(window=15).mean()

    data['RS_5'] = data['avg_5up'] / data['avg_5down']
    data['RS_15'] = data['avg_15up'] / data['avg_15down']

    data['RSI_5'] = 100 - (100/(1+data['RS_5']))
    data['RSI_15'] = 100 - (100/(1+data['RS_15']))

    data['RSI_ratio'] = data['RSI_5']/data['RSI_15']
    
    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    rsi_trace = go.Scatter(x=data.index, y=data['RSI_ratio'], mode='lines', name='RSI Ratio')

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(rsi_trace, row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

def fib_retrace(data):
      # Fibonacci constants
    max_value = data['Close'].max()
    min_value = data['Close'].min()
    difference = max_value - min_value

    # Set Fibonacci levels
    first_level = max_value - difference * 0.236
    second_level = max_value - difference * 0.382
    third_level = max_value - difference * 0.5
    fourth_level = max_value - difference * 0.618

    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], close=data['Close'], high=data['High'], low=data['Low'])])

    # Create traces for Fibonacci levels
    fig.add_trace(go.Scatter(x=data.index, y=[max_value] * len(data), mode='lines', name='Max level'))
    fig.add_trace(go.Scatter(x=data.index, y=[first_level] * len(data), mode='lines', name='Fib 0.236'))
    fig.add_trace(go.Scatter(x=data.index, y=[second_level] * len(data), mode='lines', name='Fib 0.382'))
    fig.add_trace(go.Scatter(x=data.index, y=[third_level] * len(data), mode='lines', name='Fib 0.5'))
    fig.add_trace(go.Scatter(x=data.index, y=[fourth_level] * len(data), mode='lines', name='Fib 0.618'))
    fig.add_trace(go.Scatter(x=data.index, y=[min_value] * len(data), mode='lines', name='Min level'))

    return fig