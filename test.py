import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Dash 
from jupyter_dash import JupyterDash

import plotly.graph_objects as go # or 
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from pyparsing import html_comment

data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv")

fig1 = px.scatter(data, x="Postal", y="Population", 
                  color="Population", hover_data=["State"])
fig2 = go.Figure(go.Scatter(x=data["Postal"], y=data["Population"], mode="markers",
                            marker_color=data["Population"], text=data["State"]))

# fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

#%%% Colors
colors = {
    "background": "red",
    "text": "Purple"
}
style = {
    "textAlign": "center",
    "color": colors["text"]
}
#%%% Generate table function
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'marginLeft': 'auto', 'marginRight': 'auto'})

#%%% MarkDown Support 
markdown_text = '''
### Population Introduction
America is a vast country with varied population density in many areas

**This is common in big countries**
```{python}
import pandas as pd
import sklearn
# not difficult
```
### Conclusion
As a result, this is true
Good job you did
'''
#%%% City Dropdown
city_dropdown = html.Div(children=[
   html.Label('Dropdown'),
   dcc.Dropdown(["New York City", "Montreal", "San Francisco"], "Montreal"),
   
   html.Br(),
   html.Label("Multi-Select Dropdown"),
   dcc.Dropdown(["New York City", "Montreal", "San Francisco"], ["New York", "Montreal"], multi=True),
])


#%%% City Widgets
city_widgets = html.Div(children=[
        html.Label("Radio Items"),
        dcc.RadioItems(["New York City", "Montreal", "San Francisco"], "Montreal"),
        html.Br(),

        html.Label('Checkboxes'),
        dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                      ['Montréal', 'San Francisco']
        ),

        html.Br(),
        html.Label('Text Input'),
        dcc.Input(value='MTL', type='text'),

        html.Br(),
        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
            value=5,
        ),
    ], style={'padding': 10, 'flex': 1})

#%%% App Layout Full
app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    html.H1("This is a Dash Web App", style=style),

    html.Div([
        html.H4("Please enter your name"),
        " Input: ",
        dcc.Input(id="my-input", value="initial value", type="text", style={"width": 500}),
        html.Div(id="my-output"),
    ]),
    
    # html.Div([
    #     "Rank:",
    #     dcc.Input(id="rank", value=20, type="number"),
    #     html.Button(id="rank-btn-state", n_clicks=0, children="Submit"),
    # ]),



    html.Div([ 
        dbc.Row(
            [
                dbc.Col(html.Div([
                    "Select Rank:",
                    dcc.Input(id="rank", value=20, type="number"),
                    html.Button(id="rank-btn-state", n_clicks=0, children="Submit"),
                ])),
                dbc.Col(html.Div([
                    "Select States:",
                    # dcc.Dropdown(data.State.tolist(), data.State.tolist(), multi=True, id="states"),
                    dcc.Checklist(data.State.tolist()[:10], data.State.tolist()[:3], id="states"),
                    html.Button(id="states-btn-state", n_clicks=0, children="Submit"),
                ]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([dcc.Graph(figure=fig1, id="fig1")])),
                dbc.Col(html.Div([dcc.Graph(figure=fig1, id="fig2")]))
            ]
        )
    ]),
    
    # html.Div(children=[
    #     html.Div([dcc.Graph(figure=fig1)], style={'padding': 10, 'flex': 1}),
    #     html.Div([dcc.Graph(figure=fig1)], style={'padding': 10, 'flex': 1}),  
    #     html.Div([dcc.Graph(figure=fig1)], style={'padding': 10, 'flex': 1}), 
    #     ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.H3("Here are the dropdowns for city", style=style),
    city_dropdown,
    html.Br(), html.Br(),

    html.H3("Here are some other widgets for the city", style=style),
    city_widgets,
    html.Br(), html.Br(),

    html.H3("Here is Data Table", style=style),
    html.Div("Data table (I am a div element, how large is me)", style=style),
    generate_table(data),
    html.Br(), html.Br(),

    dcc.Markdown(children=markdown_text),
    html.Br(), html.Br(),
    # card := dbc.Card(
    #     [
    #         dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
    #         dbc.CardBody(
    #             [
    #                 html.H4("Card title", className="card-title"),
    #                 html.P(
    #                     "Some quick example text to build on the card title and "
    #                     "make up the bulk of the card's content.",
    #                     className="card-text",
    #                 ),
    #                 dbc.Button("Go somewhere", color="primary"),
    #             ]
    #         ),
    #     ],
    #     style={"width": "18rem"},
    # ),
    # card := dbc.Card(
    # dbc.ListGroup(
    #     [
    #         dbc.ListGroupItem("Item 1"),
    #         dbc.ListGroupItem("Item 2"),
    #         dbc.ListGroupItem("Item 3"),
    #     ],
    #     flush=True,
    # ),
    # style={"width": "18rem"},
    # )
])


@app.callback(
    Output("my-output", "children"),
    Input("my-input", "value"),
)
def updata_output_div(input_value):
    return f"Output: {input_value}"

@app.callback(
    Output("fig1", "figure"),
    Input("rank-btn-state", "n_clicks"),
    State("rank", 'value'),
)
def update_figure_rank(n_clicks, rank):
    fig1 = px.scatter(data[data["Rank"] <= rank], x="Postal", y="Population", 
                  color="Population", hover_data=["State"])
    print("n_clicks", n_clicks)
    return fig1

@app.callback(
    Output("fig2", "figure"),
    Input("states-btn-state", "n_clicks"),
    State("states", 'value'),
)
def update_figure_state(n_clicks, states):
    fig1 = px.scatter(data[data["State"].isin(states)], x="Postal", y="Population", 
                  color="Population", hover_data=["State"])
    print("n_clicks", n_clicks)
    return fig1

## Run dependent on type of app
if str(type(app)) == "<class 'dash.dash.Dash'>":
    app.run_server(
        debug=True,
        port = 8062,
    )
else:
   app.run_server(
    mode = "inline",
    port = 8063,
    ) 
