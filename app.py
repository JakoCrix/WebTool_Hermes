#######################################
# To run this app:
# python C:\Users\Andrew\Documents\GitHub\WebTool_Hermes\app.py
#######################################
# %% Admin
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

import pandas as pd
import os
import sys
sys.path.append(os.getcwd())

# Data Extraction
from Helper.Connections_Database import connect_to_odinprod
conn_odin_str, conn_odin_obj= connect_to_odinprod()
SumComments_Raw = pd.read_sql_query("SELECT datetime_hour, title, sumcomments_hour FROM commentscount cc "
                                    "INNER JOIN subreddit_info si on cc.idsubreddit=si.idsubreddit", conn_odin_obj)

# %% Dash Admin
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# %% Dash Layout
app.layout = html.Div([
    html.H3("Welcome to Odin's Upkeep!"),

    html.Label('Subreddit of interest:'),
    dcc.RadioItems(id='temp_SubredditOfInterest',
                   value=['wallstreetbets', 'stocks'],
                   options=[{'label': 'Stocks', 'value': 'stocks'}, {'label': 'Investing', 'value': 'investing'},
                            {'label': 'Wall Street Bets', 'value': 'wallstreetbets'}, {'label': 'Stock Picks', 'value': 'Stock_Picks'},
                            {'label': 'Security Analysis', 'value': 'SecurityAnalysis'},{'label': 'Penny Stocks', 'value': 'pennystocks'}
                            ],
                   multi=True),

    html.Br()
])

@app.callback(
    dash.dependencies.Output(component_id='Subreddit_Submissions', component_property='data'),
    [dash.dependencies.Input(component_id='temp_SubredditOfInterest',component_property= 'value')]
)

def FilterSubmissions(value):
    # input_value= "stocks"
    SumComments= SumComments_Raw.copy()

    SubmissionsTable3= SubmissionsTable2[SubmissionsTable2["Subreddit"]==value]
    SubmissionsTable4= SubmissionsTable3.sort_values("CreatedDate", ascending= False)

    return SubmissionsTable4.to_dict("records")



if __name__ == '__main__':
    app.run_server(debug=True)