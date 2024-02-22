import plotly.graph_objects as go
from plotly.subplots import make_subplots
import talib

def executeIndicator(data):
    trace0 = candlesticks(data)
    bb1,bb2,bb3 = call_bollinger(data)
    atr = call_ATR(data)
    stoch1,stoch2 = call_stochastic(data)
    macd,signal,hist = call_macd(data)
    rsi,ul,ll = call_rsi(data)
    roc = call_roc(data)

    fig = make_subplots(rows=6, cols=1, shared_xaxes=True,row_heights=[1.6, 0.8, 0.8,0.8,0.8,0.8],
                   vertical_spacing=0.05, subplot_titles=('Bollinger Bands & SMA', 'ATR','Stochastic','MACD','RSI','ROC'))
    
    fig.add_trace(trace0['data'][0], row=1, col=1)
    fig.add_trace(bb1, row=1, col=1)
    fig.add_trace(bb2, row=1, col=1)
    fig.add_trace(bb3, row=1, col=1)
    fig.add_trace(atr, row=2, col=1)
    fig.add_trace(stoch1, row=3, col=1)
    fig.add_trace(stoch2, row=3, col=1)
    fig.add_trace(macd,row=4,col=1)
    fig.add_trace(signal,row=4,col=1)
    fig.add_trace(hist,row=4,col=1)
    fig.add_trace(rsi,row=5,col=1)
    fig.add_trace(ul,row=5,col=1)
    fig.add_trace(ll,row=5,col=1)
    fig.add_trace(roc,row=6,col=1)

    for y_level, line_name in zip([70, 50, 30], ['Upper Limit', 'Middle Limit', 'Lower Limit']):
        fig.add_hline(y=y_level, line_dash='dash', line_color='gray', name=line_name, row=5, col=1)

    fig.update_xaxes(row=7, col=1, rangeslider=dict(visible=True))

    fig.update_layout(
        width=800,  
        height=900
    )

    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def candlesticks(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        close=data['Close'],
        high=data['High'],
        low=data['Low']
    )])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(
        width=1700,  
        height=500
    )
    return fig

def call_ATR(data):
    atr=talib.ATR(data['High'], data['Low'], data['Close'], 20)
    atr_trace = go.Scatter(x=data.index, y=atr, mode='lines', name='ATR')
    return atr_trace

def call_stochastic(data):
    stoch1,stoch2=talib.STOCH(data['High'],data['Low'],data['Close'],fastk_period=5,slowk_period=15,slowk_matype=0,slowd_period=15,slowd_matype=0)
    stoch_trace1 = go.Scatter(x=data.index, y=stoch1, mode='lines', name='Stochastic_%D_5')
    stoch_trace2 = go.Scatter(x=data.index, y=stoch2, mode='lines', name='Stochastic_%D_15')
    return stoch_trace1, stoch_trace2

def call_macd(data):
    macd,macd_signal,macd_hist = talib.MACD(data['Close'],fastperiod= 12,slowperiod= 26,signalperiod= 9)
    macd_trace = go.Scatter(x=data.index,y=macd,mode='lines', name='MACD', marker=dict(color='royalblue')) 
    signal_trace = go.Scatter(x=data.index,y=macd_signal, mode='lines',name='SIGNAL',marker=dict(color='gold'))  
    bar_colors = ['#1E5128' if value > 0 else '#950101' for value in macd_hist]
    hist_trace = go.Bar(x=data.index, y=macd_hist,opacity=0.6,  name="MACD_HIST", marker=dict(color=bar_colors))
    return macd_trace,signal_trace,hist_trace

def call_bollinger(data):
    ub,mb,lb = talib.BBANDS(data['Close'], timeperiod=15, nbdevdn=2.0, nbdevup=2.0, matype=0)
    bollinger_trace1 = go.Scatter(x=data.index, y=ub, mode='lines', name='Upperband')
    bollinger_trace2 = go.Scatter(x=data.index, y=mb, mode='lines', name='SMA_15')
    bollinger_trace3 = go.Scatter(x=data.index, y=lb, mode='lines', name='Lowerband')
    return bollinger_trace1, bollinger_trace2, bollinger_trace3

def call_roc(data):
    roc=talib.ROC(data['Close'],timeperiod=20)
    roc_trace = go.Scatter(x=data.index, y=roc, mode='lines', name='RC')
    return roc_trace

def call_rsi(data):
    rsi = talib.RSI(data['Close'],timeperiod=20)
    rsi_trace = go.Scatter(x=data.index,y=rsi,mode='lines',name='RSI',line=dict(color='blue', width=2))
    ul = go.Scatter(x=data.index, y=[70] * len(data.index), mode='lines', line=dict(color='grey', width=2, dash='dash'), name='UpperBound')
    ll = go.Scatter(x=data.index, y=[30] * len(data.index), mode='lines', line=dict(color='grey', width=2, dash='dash'), name='LowerBound')
    return rsi_trace,ul,ll

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