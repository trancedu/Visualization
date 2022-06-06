import dash
import pandas as pd
import yfinance as yf
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

#%% Data Download Section

def download_data(ticker):
    myTicker = yf.Ticker(ticker)
    hist = myTicker.history(period="max")

    hist = hist.reset_index()
    hist['Date'] = pd.to_datetime(hist['Date'], errors = 'coerce')
    return hist

    # hist['Date'].max()

ticker = "AAPL"
hist = download_data(ticker)


#%% Graph generation
fig = px.scatter(hist, y="Open", x='Date')

# The update_layout method allows us to give some formatting to the graph
fig.update_layout(
    title_text = "Time Series Plot of {}".format(ticker),
    title_x = 0.5,
    yaxis = {
        'title': 'Price'}
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     # stepmode="backward"
                     ),
                dict(count=6,
                     label="6m",
                     step="month",
                     # stepmode="backward"
                     ),
                dict(count=1,
                     label="YTD",
                     step="year",
                     # stepmode="todate"
                     ),
                dict(count=1,
                     label="1y",
                     step="year",
                     # stepmode="backward"
                     ),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        # type="date",
        # title='This is a date'
    )
)

#%% Dash app
app = Dash()

app.layout = html.Div(
    [
        "See how it will be displayed",
        html.Center(html.H4('My Very First Dash App - Yey!!!')),
        html.Br(),
        dcc.Input(
            id="my-input",
            type="text",
            placeholder="Please input stock symbol name: "
        ),

        html.Br(),
        html.Div(id='my-output'),

        dcc.Dropdown(
            options=[
                dict(label="GOOG", value=0),
                dict(label="AAPL", value=1),
                dict(label="SPX", value=2),
            ],
            placeholder = "Select symbol"
        ),



        html.Div('''
             This app displays a graph of the entire price history of {}.'''.format(ticker),
             style = {
                 'width': '60%',
                 'text-align': 'center',
                 'margin-left': 'auto',
                 'margin-right': 'auto',
             }
        ),
        
        dcc.Graph(figure = fig, id="graphic")


        
        
    ],  #I could also put the list comprehension here
    style ={
        'margin': '2em',
        'border-radius': '1em',
        'border-style': 'solid', 
        'padding': '2em',
        'background': '#ededed'
    }
)


@app.callback(
    Output(component_id="graphic", component_property="figure"),
    Input(component_id="my-input", component_property="value")
)
def update_output_div(input_value):
    # return f'Output: {input_value}'
    ticker = input_value if input_value else "AAPL"
    hist = download_data(ticker)
    #%% Graph generation
    fig = px.scatter(hist, y="Open", x='Date')

    # The update_layout method allows us to give some formatting to the graph
    fig.update_layout(
        title_text = "Time Series Plot of {}".format(ticker),
        title_x = 0.5,
        yaxis = {
            'title': 'Price'}
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        # stepmode="backward"
                        ),
                    dict(count=6,
                        label="6m",
                        step="month",
                        # stepmode="backward"
                        ),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        # stepmode="todate"
                        ),
                    dict(count=1,
                        label="1y",
                        step="year",
                        # stepmode="backward"
                        ),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            # type="date",
            # title='This is a date'
        )
    )
    return fig



print('About to start...')
                
app.run_server(
    debug = True,
    port = 8061
)


# %%
