import pandas as pd
import plotly.graph_objects as go

#%% plotly
class graphs():
    
    @staticmethod
    def get_empty_fig():
        fig = go.Figure()
        
        fig.update_layout(
            # this is a function taking multiple kwargs where complex args have to be passed as dictionaries
            paper_bgcolor = '#ededed',
            plot_bgcolor = '#ededed',
            autosize = True,
            height = 400,
            xaxis = {
                'showline': True, 
                'linewidth': 1,
                'linecolor': 'black',
                'gridcolor': '#ededed',
                'rangemode': 'tozero',
            },
            yaxis = {
                'showline': True, 
                'linewidth': 1,
                'linecolor': 'black',
                'gridcolor': '#ededed',
                'rangemode': 'tozero',
            }
        )
        
        return(fig)
    
    @staticmethod
    def get_single_scatter(x, y, title, name = 'sc1'):
        # with the full graphics object, we can create a template figure which is fully flexible.
        fig = go.Figure()
        
        # the new figure, is now ready to have anything added to it:
        fig.add_trace(go.Scatter(y=y, x=x, name = name))
        
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
                'title': '',     # maybe add this later?
                'showline': True, 
                'linewidth': 1,
                'linecolor': 'black'
            },
            yaxis = {
                'showline': True, 
                'linewidth': 1,
                'linecolor': 'black'
            }
        )
        
        # This updates the data portion
        fig.update_traces(line = {'color': 'gray', 'width': 1})
        
        return(fig)