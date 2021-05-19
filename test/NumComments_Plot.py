# %% Admin
import pandas as pd
import os
import sys
import plotly.express as px
from datetime import date

# Data Extraction
from Helper.Connections_Database import connect_to_odinprod
conn_odin_str, conn_odin_obj= connect_to_odinprod()
SumComments_Raw = pd.read_sql_query("SELECT datetime_hour, title, sumcomments_hour FROM commentscount cc "
                                    "INNER JOIN subreddit_info si on cc.idsubreddit=si.idsubreddit", conn_odin_obj)

# Filters
subreddits_list = ["stocks", "wallstreetbets"]
start_date = date(2021,1,1)
end_date = date(2021,1,25)

SumComments2= SumComments_Raw[SumComments_Raw["title"].isin(subreddits_list)]

fig = px.line(SumComments2, x="datetime_hour", y="sumcomments_hour", color='title')
fig.update_layout(xaxis_range=[start_date,end_date])
fig.show()