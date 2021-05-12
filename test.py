# %% Admin
import pandas as pd
import os
import sys
sys.path.append(os.getcwd())

import plotly.express as px


# Data Extraction
from Helper.Connections_Database import connect_to_odinprod
conn_odin_str, conn_odin_obj= connect_to_odinprod()
SumComments_Raw = pd.read_sql_query("SELECT datetime_hour, title, sumcomments_hour FROM commentscount cc "
                                    "INNER JOIN subreddit_info si on cc.idsubreddit=si.idsubreddit", conn_odin_obj)

fig = px.line(SumComments_Raw, x="datetime_hour", y="sumcomments_hour", color='title')


fig.show()