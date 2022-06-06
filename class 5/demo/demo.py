import dash
import pandas as pd
import yfinance as yf
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, State

# user define
import resources.faang as faang
import resources.graph as graph

#%% Data Download Section
DATA = faang.faangs().data
GX = graph.graphs()

#%% Dash app
app = Dash(
    # prevent_initial_callbacks = True
)

app.layout = html.Div(
    [
        html.Center(html.H4('FANG Stock Analyzer')),
        
        html.Div(
            'Simple plotting tool for the FAANG stocks',
             style = {
                 'width': '60%',
                 'text-align': 'center',
                 'margin-left': 'auto',
                 'margin-right': 'auto',
             }
        ),
        
        html.Div(
            [
                dcc.Dropdown(
                    options = [{'label': v, 'value': v} for v in DATA['Stock'].drop_duplicates()],
                    value = 'FB',
                    id = 'stocks',
                    placeholder = 'Select a stock',
                    multi = False,
                    style = {
                         'width': '15em'
                    }
                ),
                dcc.RadioItems(
                    options = [{'label': v, 'value': v} for v in DATA.columns if v not in ['Date'] and v.find('_g') < 1],
                    value = 'Open',
                    id = 'series',
                ),
                dcc.Checklist(
                    options = [{'label': 'plot growth', 'value': 'plot growth'}],
                    value = [''],
                    id = 'type',
                )
            ],
            style = {
                 'width': 'auto',
                 'text-align': 'left',
                 'margin-left': '2em',
                 'margin-right': 'auto',
             }
        ),
        
        dcc.Graph(figure = GX.get_empty_fig(), id = 'fig')
        
        
    ],  #I could also put the list comprehension here
    style ={
        'margin': '2em',
        'border-radius': '1em',
        'border-style': 'solid', 
        'padding': '1em',
        'background': '#ededed'
    }
)

@app.callback(
    Output('fig', 'figure'),
    [
        Input('stocks', 'value'),
        Input('series', 'value'),
        Input('type', 'value'),
    ]
    
)
def update_graph(stock, series, series_type):
    
    data = DATA.loc[DATA['Stock'] == stock].copy()    #just in case
    
    print(series_type)
    if series_type:
        print('')
    
    fig = GX.get_single_scatter(data['Date'].to_list(), data[series].to_list(), '{} {}'.format(stock, series), name = 'Date')
    
    print('Did it trigger?')
    
    return(fig)

app.run_server(
    debug = True,
    port = 8090
)

