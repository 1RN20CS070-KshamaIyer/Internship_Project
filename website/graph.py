import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

def executeIndicator(data):

    trace0 = candlesticks(data)
    trace1 = call_bollinger(data)
    trace2 = call_ATR(data)
    trace3 = call_stochastic(data)
    trace4 = call_macd(data)
    trace5 = call_rsi(data)
    trace6 = call_rac(data)

    fig = make_subplots(rows=6, cols=1, shared_xaxes=True,row_heights=[1.6, 0.8, 0.8,0.8,0.8,0.8],
                   vertical_spacing=0.05, subplot_titles=('Bollinger Bands & SMA', 'ATR','Stochastic','MACD','RSI','ROC'))

    fig.add_trace(trace0['data'][0], row=1, col=1)
    fig.add_trace(trace1['data'][1], row=1, col=1)
    fig.add_trace(trace1['data'][2], row=1, col=1)
    fig.add_trace(trace1['data'][3], row=1, col=1)
    fig.add_trace(trace2['data'][1], row=2, col=1)
    fig.add_trace(trace3['data'][0], row=3, col=1)
    fig.add_trace(trace3['data'][1], row=3, col=1)
    fig.add_trace(trace4['data'][1],row=4,col=1)
    fig.add_trace(trace4['data'][2],row=4,col=1)
    fig.add_trace(trace5['data'][1],row=5,col=1)
    fig.add_trace(trace6['data'][1],row=6,col=1)

    for y_level, line_name in zip([70, 50, 30], ['Upper Limit', 'Middle Limit', 'Lower Limit']):
        fig.add_hline(y=y_level, line_dash='dash', line_color='gray', name=line_name, row=5, col=1)

    fig.update_xaxes(row=7, col=1, rangeslider=dict(visible=True))

    # Update layout
    fig.update_layout(
        width=1000,  
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
    return fig

def atr(high, low, close, n=14):
    tr = np.amax(np.vstack(((high - low).to_numpy(), (abs(high - close)).to_numpy(), (abs(low - close)).to_numpy())).T, axis=1)
    return pd.Series(tr).rolling(n).mean().to_numpy()

def call_ATR(data):
    data['ATR']=atr(data['High'], data['Low'], data['Close'], 20)

    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    atr_trace = go.Scatter(x=data.index, y=data['ATR'], mode='lines', name='ATR')


    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(atr_trace, row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)
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
    stoch_trace1 = go.Scatter(x=data.index, y=data['Stochastic_%D_5'], mode='lines', name='Stochastic_%D_5')
    stoch_trace2 = go.Scatter(x=data.index, y=data['Stochastic_%D_15'], mode='lines', name='Stochastic_%D_15')

    fig = make_subplots(rows=1, cols=1, vertical_spacing=0.5,row_heights=[0.8])

    fig.add_trace(stoch_trace1, row=1, col=1)
    fig.add_trace(stoch_trace2, row=1, col=1)
    return fig

def call_macd(data):

    # Calculate MACD components
    data['12Ewm'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['26Ewm'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['26Ewm'] - data['12Ewm']
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Create candlestick chart
    main_fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            close=data['Close'],
            high=data['High'],
            low=data['Low']
        )
    ])

    # Create MACD and signal line traces
    macd_trace = go.Scatter(
        x=data.index,
        y=data['MACD'],
        mode='lines',
        name='MACD',
        line=dict(color='blue', width=2)
    )
    signal_trace = go.Scatter(
        x=data.index,
        y=data['Signal'],
        mode='lines',
        name='Signal',
        line=dict(color='orange', width=2)
    )

    # Create subplots and add traces
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5, row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(macd_trace, row=2, col=1)
    fig.add_trace(signal_trace, row=2, col=1)

    # Update layout
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=4
        )
    )

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
    main_fig.update_layout(xaxis_rangeslider_visible=False)
    return main_fig

def call_rac(data):
    data['RC'] = data['Close'].pct_change(periods = 20)

    main_fig=go.Figure(data=[go.Candlestick(x=data.index,open=data['Open'],close=data['Close'],high=data['High'],low=data['Low'])])
    racd_trace = go.Scatter(x=data.index, y=data['RC'], mode='lines', name='RC')

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(racd_trace, row=2, col=1)

    # Update layout for better visualization
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def call_rsi(data):
    length = 14  # Length for RSI calculation

    # Calculate gains and losses using diff and rolling window
    gains = data['Close'].diff()
    gains[gains < 0] = 0  # Set negative gains to zero
    losses = -data['Close'].diff()
    losses[losses < 0] = 0  # Set negative losses to zero
    avg_gain = gains.rolling(window=length).mean()
    avg_loss = losses.rolling(window=length).mean()

    # Calculate RS and RSI
    data['RS'] = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + data['RS']))

    # Create candlestick chart
    main_fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            close=data['Close'],
            high=data['High'],
            low=data['Low']
        )
    ])

    # Create RSI and smoothed RSI traces
    rsi_trace = go.Scatter(
        x=data.index,
        y=data['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='blue', width=2)
    )

    # Create subplots and add traces
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5, row_heights=[0.8, 0.2])
    fig.add_trace(main_fig.data[0], row=1, col=1)
    fig.add_trace(rsi_trace, row=2, col=1)

    # Add horizontal reference lines with row/col specification
    for y_level, line_name in zip([70, 50, 30], ['Upper Limit', 'Middle Limit', 'Lower Limit']):
        fig.add_hline(y=y_level, line_dash='dash', line_color='gray', name=line_name, row=2, col=1)

    # Update layout
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=4
        )
    )

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