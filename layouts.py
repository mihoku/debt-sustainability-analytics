import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import dash_table
from plotly.subplots import make_subplots
#import pyodbc 
import pandas as pd
import pathlib
import json
import numpy as np
from basic1 import BASIC1
from realism import REALISM

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data-source").resolve()
OTHER_PATH = PATH.joinpath("other-datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath('change in debt.csv'),low_memory=False, sep=";", header=0)
x = df['Tahun']

BASIC2 = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card()),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card()),], style={"marginTop": 30}),
        #dbc.Row(
            #[
               # dbc.Col(LEFT_COLUMN, md=4, align="center"),
                #dbc.Col(dbc.Card(TOP_BANKS_PLOT), md=8),
            #],
            #style={"marginTop": 30},
        #),
        #dbc.Card(),
        #dbc.Row([dbc.Col([dbc.Card()])], style={"marginTop": 50}),
    ],
    className="mt-12",
)

layout1 = html.Div(children=[BASIC1])
layout2 = html.Div(children=[BASIC2])
layout3 = html.Div(children=[REALISM])
layout4 = html.Div(children=[BASIC2])
layout5 = html.Div(children=[BASIC2])
     
#layout1 = html.Div([
#    html.Div([
#            html.H5("Persebaran Peserta JKN Menurut Provinsi",style={"font-weight":"bold"}),
#            dcc.Graph(figure=fig),
#        ], className="pretty_container twelve columns"),
#    ], className="row")
