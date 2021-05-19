#######################################
# To run this app:
# python C:\Users\Andrew\Documents\GitHub\WebTool_Hermes\app.py
#######################################
# %% Admin
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import sys
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

import plotly.express as px
sys.path.append(os.getcwd())

# Data Extraction
from Helper.Connections_Database import connect_to_odinprod
conn_odin_str, conn_odin_obj= connect_to_odinprod()
SumComments_Raw = pd.read_sql_query("SELECT datetime_hour, title, sumcomments_hour FROM commentscount cc "
                                    "INNER JOIN subreddit_info si on cc.idsubreddit=si.idsubreddit", conn_odin_obj)

Tempdaterange_min= min(SumComments_Raw.datetime_hour).date()
Tempdaterange_max= max(SumComments_Raw.datetime_hour).date()
Tempdaterange_max+relativedelta(months=-3)

# %% Dash Admin
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# %% Dash Layout
app.layout = html.Div([
    html.H3("Welcome to Odin's Upkeep!"),

    html.Div([
        html.Label('Subreddit of interest:'),
        dcc.Dropdown(id='OfInterest_Subreddits',
                     value=['stocks', 'wallstreetbets'], multi=True,
                     options=[{'label': 'Stocks', 'value': 'stocks'}, {'label': 'Investing', 'value': 'investing'},
                              {'label': 'Wall Street Bets', 'value': 'wallstreetbets'}, {'label': 'Stock Picks', 'value': 'Stock_Picks'},
                              {'label': 'Security Analysis', 'value': 'SecurityAnalysis'}, {'label': 'Penny Stocks', 'value': 'pennystocks'}]
                     )
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Date Picker:'),
        dcc.DatePickerRange(id='OfInterest_DateRange',
                            display_format='D/M/Y',
                            min_date_allowed=Tempdaterange_min, max_date_allowed=Tempdaterange_max,
                            start_date=Tempdaterange_max+relativedelta(months=-3), end_date=Tempdaterange_max,
                            initial_visible_month=date(2021, 1, 1),
                            )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    html.Br(),

    dcc.Graph(id='indicator-graphic'),

])


# Functions
@app.callback(
    Output(component_id='indicator-graphic', component_property='figure'),
    Input(component_id='OfInterest_Subreddits', component_property='value'),
    [Input(component_id='OfInterest_DateRange', component_property='start_date'),
     Input(component_id='OfInterest_DateRange', component_property='end_date')]
)
def update_DashPlot(subreddits_list, start_date, end_date):
    # Admin
    SumComments2 = SumComments_Raw[SumComments_Raw["title"].isin(subreddits_list)].copy()
    startdate2 = date.fromisoformat(start_date)
    enddate2 = date.fromisoformat(end_date)

    fig = px.line(SumComments2, x="datetime_hour", y="sumcomments_hour", color='title')
    fig.update_layout(xaxis_range=[startdate2, enddate2])

    return fig


# End
if __name__ == '__main__':
    app.run_server(debug=True)