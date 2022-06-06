import plotly.graph_objects as go
import pandas as pd
import numpy as np

def update_graph(fig, title, x_axis, name):
    fig.update_layout(
        # this is a function taking multiple kwargs where complex args have to be passed as dictionaries
        title = {
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'font': {'size': 22}
        },
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
        autosize = True,
        height = 400,
        xaxis = {
            'title': x_axis,
            'showline': True, 
            'linewidth': 1,
            'linecolor': 'black'
        },
        yaxis = {
            'title': name,
            'showline': True, 
            'linewidth': 1,
            'linecolor': 'black'
        }
    )
    
    return(fig)

def get_graph(x, y, name, title, x_axis):
    fig = go.Figure()
    
    # the new figure, is now ready to have anything added to it:
    fig.add_trace(go.Scatter(y=y, x=x, name = name))
    
    fig = update_graph(fig, title, x_axis, name)
    
    return(fig)

def make_tree(px):
    N = len(px)
    
    y = pd.DataFrame(np.zeros((N, N)))
    y.iloc[:,-1] = range(N, 0, -1)
    
    for i in range(N-1, 0, -1):
        y.iloc[:, i - 1] = [(y.iloc[j, i] + y.iloc[j + 1, i])/2  if j < i else 0
                              for j in range(N)]
    
    px = pd.Series(px.T.to_numpy().flatten())
    x = pd.Series(pd.DataFrame([range(N)] * (N)).T.to_numpy().flatten())
    y = pd.Series(y.T.to_numpy().flatten())
    
    data = pd.DataFrame({'px': px, 'x': x, 'y': y}).copy().dropna(how = 'any')
    
    lines = data.copy()
    lines = lines.set_index('x')
    
    line_x = []
    line_y = []
    
    for i in range(1, N):
        if  i==1:
            for y in lines.loc[i, 'y']:
                line_x += [0, i, None]
                line_y += [lines.iloc[0]['y'], y, None]
        else:
            for p, ym1 in enumerate(lines.loc[i - 1, 'y']):
                for j in range(2):
                    
                    y = lines.loc[i, 'y'].iloc[p+j]
                    line_x += [i-1, i, None]
                    line_y += [ym1, y, None]
    
    # Here is the data for the grah
    Xn = data['x']
    Yn = data['y']
    Xe = line_x
    Ye = line_y
    labels = data['px'].round(2)
    
    # make the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       name=' ',
                       line=dict(color='black', width=1),
                       ))
    fig.add_trace(go.Scatter(x=Xn,
                      y = Yn,
                      mode = 'markers',
                      name = 'Binomial Option Pricing Leaves',
                      marker = dict(symbol='circle-dot',
                                    size=18,
                                    color = '#DB4551',
                                    # line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                      text = labels,
                      hoverinfo='text',
                      opacity=0.8
                      ))
    
    fig = update_graph(fig, 'Binomial Option Pricing Leaves', 'Leaves', None)
    return(fig)