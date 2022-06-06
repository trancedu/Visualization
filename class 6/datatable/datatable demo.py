import yfinance as yf
import dash

from dash import html, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
from dash.dash_table import DataTable, FormatTemplate, Format
from datetime import datetime as dt

def get_dashtable(df, tableID, cond_style = [], selectable = None, row_ids = None, filtering = 'none', sorting = 'none', scroll = None, 
                  row_style = [], editable = [], cond_format = None, page_action = 'native', export = False, ddown = {}):
    '''
    This is a master datatable creation function.
    It simplyfies the code by consolidating the requests and handling each table's verson based on the args

    Parameters
    ----------
    df :            pd.DF       The data to show
    tableID :       STR         The dash element ID
    row_ids :       LIST        Allows for an identifier to be assigned to each row
    page_action :   STR         Either 'native' or 'none'; 'native' uses dash default page size of 25 rows/page
    export :        BOOL        Either True or False; this makes the table fully exportable.
    
    selectable :    STR         Either 'multi' or None. Multu allows for row selections
    filtering :     STR         Either 'native', 'none', or 'custom'; Make sure it is 'none' and not None. 'native' uses dash's filtering;
                                'custom' needs to be enabled to induce custom filtering. 'none' removes the filtering boxes
    sorting :       STR         Either 'native', 'none', or 'custom'; Make sure it is 'none' and not None. 'native' uses dash's filtering;
                                'custom' needs to be enabled to induce custom filtering. 'none' removes the filtering boxes
    scroll :        STR         Either None, 'overflow-x', 'overflow-y'; this applies the css overflow scroll to the table itself
    
    cond_style :    LIST        A list of the conditional styles applied by column names
    row_style :     LIST        A list of the conditional styles applied by row ids
    editable :      LIST        A list of the column names that can be editable; all other columns are lock for editing
    cond_format :   DICT        A dictionary containing the columns names (values) and the type of format (keys). Available formats are:
                                    ['commas', 'decimals', 'money']
    ddown :         DICT        A dictionary containing the columns names that would have a dropdown (keys) and a LIST of dash dropdown options 
                                dictionary values -> [{'label': 'value':}] <- to be displayed in the columns (values). 
                                The dropdown will be the same for the entire column.
        
    '''
    
    if cond_format:
        print(cond_format)
        commas   = cond_format['commas']
        decimals = cond_format['decimals']
        money    = cond_format['money']
        formats = {
            **{m: FormatTemplate.money(3) for m in money}, 
            **{c: Format.Format(group=',') for c in commas},
            **{c: Format.Format(precision = 4, scheme = Format.Scheme.fixed) for c in decimals}
        }
        
        cols = [
            {'id': c, 'name': c, 'editable': True if c in editable + list(ddown.keys()) else False, 'type': 'numeric', 'format': formats[c], 
                 'presentation': 'dropdown' if c in ddown.keys() else 'input'} if c in formats.keys() else
            {'id': c, 'name': c, 'editable': True if c in editable + list(ddown.keys()) else False, 
                 'presentation': 'dropdown' if c in ddown.keys() else 'input'} for c in df.columns
        ] 
        
        print('These are the columns: ', cols)
        
    else: # list with id and name, whether it is editable, presentation
        cols = [{'id': c, 'name': c, 'editable': True, 'presentation': 'dropdown' if c in ddown.keys() else 'input'} if c in editable else 
                {'id': c, 'name': c, 'editable': True, 'presentation': 'dropdown' if c in ddown.keys() else 'input'} for c in df.columns]
    
    contents = DataTable(
        data=df.to_dict('records'),
        #NOTE: in order to access the id, I need a row with the id -> ID or Id will not work
        columns = cols,
        
        style_table = {
            'border': 'none',
            'border-collapse': 'collapse',
            'overflowX': scroll,
            },
        style_cell={
            'border': 'none',
            'fontSize': '12px', 
            'boxShadow': '0 0',
            'height': 'auto',
            'width': 'auto',
            'whiteSpace': 'normal',
            'textAlign': 'center'
            },
        
        style_cell_conditional = cond_style, # column
        style_data_conditional = row_style, # take on entire row
        style_as_list_view = True,
        style_header={
            'border': 'none',
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'borderBottom': '1px solid black',
            'font-size' : '14px'
        },
        style_data={'whiteSpace': 'pre-line', 'height': 'auto'},
        
        # #EXTRA OPTIONS
        id = tableID,
        row_selectable  = 'single',
        # editable = True,
        filter_action   = filtering,
        # sort_action     = 'none',
        sort_action     = sorting,
        page_action     = 'native',
        export_format   = "xlsx" if export == True else 'none',
        filter_options  = {'case': 'insensitive'},
        dropdown        = ddown,

    )
    return(contents)

def get_formatted_table(df):
    # This does an interchangable color
    row_style = [
            {
                'if': {'row_index': 'odd'}, #if statement
                'backgroundColor': '#eaf1f8'
            },
            
        ]
    
    # this can be applied to format the columns individually
    cond_style = [
        {
            'if': {'column_id': c},
            'textAlign': 'right',
            'width': '5em',
        } for c in ['Date', 'Dividends', 'Stock Splits']
    ] + [
        {
            'if': {'column_id': c},
            'color': 'blue',
        } for c in ['Close']
    ]
    
    editable_list = ['Dividends'] # here editable
        
    # this handles numerical formats
    cond_format = {
        'commas'    : ['Volume'],
        'decimals'  : ['Open', 'High', 'Low'],
        'money'     : ['Close']
    }
    
    table = get_dashtable(df, 'table_id', cond_style = cond_style, selectable = None, sorting = 'native', 
        row_style = row_style, cond_format = cond_format, filtering = 'custom', page_action = 'native',
        editable = editable_list, export = True
    )
    
    print('\n\n\n', table)
    
    return(table)

def get_unformatted_table(df):
    table = get_dashtable(df, 'table_id')
    return(table)
    
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    prevent_initial_callbacks = True,
)

#%% getting some data
msft = yf.Ticker("MSFT")
df = msft.history(period="max")

# dates are easy to format directly
df = df.reset_index()
df['Date'] = df['Date'].map(dt.date)
df['Close'] = df['Close'].astype(float)

df = df.iloc[1:10]

# df['Open'] = df['Open'].map(lambda x : '{:0.2f}'.format(x))

#%% the app
app.layout = html.Div(
    [
        html.H1('Dash DataTable Demo App'),
        dbc.Checklist(
            options=[
                {"label": "Formatted", "value": 1},
            ],
            value=[],
            id = "format",
            inline = True,
            switch = True,
        ),
        html.Br(),
    
        html.Div(get_unformatted_table(df), id='table'),
        
    ], style = {'margin': '1em', 'padding': '1em'}
)

#%% Callback
@app.callback(
    Output('table', 'children'),
    Input('format', 'value')
)
def format_table(formatted):
    print(formatted)
    if formatted:
        return(get_formatted_table(df))
    else:
        
        return(get_formatted_table(df))

if __name__ == '__main__':
    app.run_server(
        debug=True
    )


