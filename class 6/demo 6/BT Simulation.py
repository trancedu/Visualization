import dash
import pandas as pd

from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc 

# BT model
import resources.bt as bt
import resources.graph as my_graph
bt.tester()

#%% Dash HTML Components
def get_input(mytype, name, pg = 'c', step = 0.01, options = None):
    '''
    Parameters
    ----------
    pg : STR, optional
        Either c or l representing the convergence or the leaves pages. The default is 'c'.
    '''
    pg = '_' + pg
    
    if mytype == 'dropdown':
        content = [
            # html.Label(name + ':'),
            dbc.Label(name + ':'),
            dbc.Select(id = name.lower().replace(' ', '_') + '_dd' + pg, 
                       options = [{'label': op, 'value': op} for op in options]),
        ]
    else:
        # probably should be an elif
        content = [
            dbc.Label(name + ':'),
            dbc.Input(id = name.lower().replace(' ', '_') + '_num' + pg, type="number", step = step),
        ]
    return(content)

def get_inputs(pg = 'c'):
    # switch function
    contents = [
        dbc.Row(
            [
                dbc.Col(width = True), # half on each side, padding
                dbc.Col(get_input('dropdown', 'Option Type', options = ['Call', 'Put'], pg = pg), width = 2),
                dbc.Col(get_input('num', 'Spot Price', pg = pg), width = 2),
                dbc.Col(get_input('num', 'Strike Price', pg = pg), width = 2),
                dbc.Col(get_input('num', 'Risk Free Rate', pg = pg), width = 2),
                dbc.Col(get_input('num', 'Volatility', pg = pg), width = 2),
                dbc.Col(width = True),
            ], 
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(width = True),
                dbc.Col(get_input('num', 'Dividend Yield', pg = pg), width = 2),
                dbc.Col(get_input('num', 'Time', step = 0.25, pg = pg), width = 2),
                dbc.Col(get_input('num', 'Iterations', step = 1, pg = pg), width = 2),
                dbc.Col(get_input('dropdown', 'Execution Style', options = ['American', 'European'], pg = pg), 
                                    width = 2) if pg == 'c' else dbc.Col(width = True),
                dbc.Col(width = True),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(width = True),
                dbc.Col(dbc.Button("Reset", color="primary", className="me-1",
                                   id = 'reset_btn_{}'.format(pg)), width = 'auto'),
            ]
        )
    ]
    return(contents)

def get_conv():
    contents = [
        html.Center(html.H3('Binomial Tree Option Price Convergence')),
        
        # This is new, grid placement using bootstrap
        dbc.Card(
            # dbc.CardHeader('Test'),
            dbc.CardBody(
                get_inputs(), id = 'conv_inputs'
            ), className = 'inputs_card'
        ),
                
        html.Hr(),
                
        dcc.Loading(
            html.Div(id="graph_div_c"),
            id="graph_ldg",
            # type="default",
            # type="graph",
            # type="cube",
            # type="circle",
            type="dot",
        ),
    ]  #I could also put the list comprehension here
    return(contents)

def get_tree():
    contents = [
        html.Center(html.H3('Binomial Tree Option Pricing Tree')),
        
        # This is new, grid placement using bootstrap
        dbc.Card(
            # dbc.CardHeader('Test'),
            dbc.CardBody(
                get_inputs('l')
            ), id = 'leaves_inputs', className = 'inputs_card'
        ),
                
        html.Hr(),
                
        dcc.Loading(
            html.Div(id="graph_div_l"),
            id="graph_ldg_l",
            # type="default",
            # type="graph",
            # type="cube",
            # type="circle",
            type="dot",
        ),
    ]  #I could also put the list comprehension here
    return(contents)

#%% Dash app
app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    prevent_initial_callbacks = True,
)

#%% Persistent HTML
top_menu = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div("Binomial Option Pricing Tools", 
                             style = {'font-size': '1.4em', 'font-weight': 'bold'},
                    ), width = 'auto'),
                dbc.Col(width=True),
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavLink("Convergence", href="conv", id="conv_pg", active=True),
                            dbc.NavLink("leaves", href="leaves", id="leaves_pg"),
                        ],
                        
                        # options
                        # vertical = True,
                        pills = True,
                    ), width = 'auto'
                ), 
            ], align = 'center'
        ),
    ], id = 'top_menu_div', className = 'top_menu'
)

app.layout = html.Div(
    [
         dcc.Location(id="url"),    
         top_menu,
         html.Div(id = 'main_div', className = 'main_contents'),
    ], 
)

#%% Callbacks
pg_ids = ["conv_pg", 'leaves_pg']
@app.callback(
    [Output(f"{pg_id}", "active") for pg_id in pg_ids] + [Output('main_div', 'children')], 
    [
        Input("url", "pathname"),
    ],
)
def main_loadings(pathname):
    # this is a linux thing 
    
    print(pathname)
    
    if pathname.find("leaves") >= 0:
        return(False, True, get_tree())
    else:
        # because at lunch there is no page selected
        return(True, False, get_conv())
        
#%%% Convergence
components_c = ['spot_price_num_c', 'strike_price_num_c', 'risk_free_rate_num_c', 'volatility_num_c', 
                'dividend_yield_num_c', 'time_num_c', 'iterations_num_c']
components_v = ['option_type_dd_c', 'execution_style_dd_c']
@app.callback(
    Output('graph_div_c', 'children'),
    [ 
        Input('{}'.format(c), 'value') for c in components_v] + [
        Input('{}'.format(c), 'value') for c in components_c] + [
    ] 
)
def get_graph_c(*args):
    # import time
    # time.sleep(3)
    
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        comp_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if comp_id == 'reset_btn':
        # this should clean everything up
        content = html.Center(dbc.Alert("Still working on it", color="danger", dismissable = True, duration = 5000,
                            className = 'my_alert'))
    else:
        '''
        The idea is, as long as all values have been filled/selected I can process the graph, otherwise, 
        alert the user that more selections are needed
        '''
        if all(args):
            # here I should call the graph
            
            px = bt.BinomialTreeConvergence(
                option_type = args[0][0], 
                S0 = args[2], 
                K = args[3], 
                r = args[4],
                sigma = args[5], 
                q = args[6], 
                T = args[7],
                N = args[8], 
                american = 'true' if args[1] == 'American' else 'false'
            )
            
            content = dcc.Graph(figure = my_graph.get_graph(
                                [p + 1 for p in range(len(px))], 
                                y = px, 
                                name = 'price convergence', 
                                title = 'Price Convergence for {} tree splits'.format(args[8]),
                                x_axis = 'Iterations'
                            ))
            
        else:
            # here, I just want to print an alert
            content = html.Center(dbc.Alert("Please continue to make your selections", color="secondary", 
                                dismissable = True, duration = 5000, className = 'my_alert'))
    
    return(content)

@app.callback(
    Output('conv_inputs', 'children'),
    Input('reset_btn_c', 'n_clicks')
)
def reset_c(n):
    return(get_inputs())

#%%% leaves
components_l = ['spot_price_num_l', 'strike_price_num_l', 'risk_free_rate_num_l', 'volatility_num_l', 
                'dividend_yield_num_l', 'time_num_l', 'iterations_num_l']
components_v = ['option_type_dd_l']
@app.callback(
    Output('graph_div_l', 'children'),
    [ 
        Input('{}'.format(c), 'value') for c in components_v] + [
        Input('{}'.format(c), 'value') for c in components_l] + [
    ] 
)
def get_graph_l(*args):
    # import time
    # time.sleep(3)
    
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        comp_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if comp_id == 'reset_btn':
        # this should clean everything up
        content = html.Center(dbc.Alert("Still working on it", color="danger", dismissable = True, duration = 5000,
                            className = 'my_alert'))
    else:
        '''
        The idea is, as long as all values have been filled/selected I can process the graph, otherwise, 
        alert the user that more selections are needed
        '''
        if all(args):
            # here I should call the graph
            print(args)
            px, p = bt.BinomialTreePayoff(
                option_type = args[0][0], 
                S0 = args[1], 
                K = args[2], 
                r = args[3],
                sigma = args[4], 
                q = args[5], 
                T = args[6],
                N = args[7], 
            )
            
            content = dcc.Graph(figure = my_graph.make_tree(px))
            print(content)
        else:
            # here, I just want to print an alert
            content = html.Center(dbc.Alert("Please continue to make your selections", color="secondary", 
                                dismissable = True, duration = 5000, className = 'my_alert'))
    
    return(content)



@app.callback(
    Output('leaves_inputs', 'children'),
    Input('reset_btn_c', 'n_clicks')
)
def reset_l(n):
    return(get_inputs())
#%% Run
app.config.suppress_callback_exceptions = True
app.run_server(
    port = 8063,
    debug = True
)

