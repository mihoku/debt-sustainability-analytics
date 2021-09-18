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
from basic2 import BASIC2
from realism import REALISM

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data-source").resolve()
OTHER_PATH = PATH.joinpath("other-datasets").resolve()
ASSETS_PATH = PATH.joinpath("assets").resolve()

df = pd.read_csv(DATA_PATH.joinpath('change in debt.csv'),low_memory=False, sep=";", header=0)
x = df['Tahun']

layout0 = dbc.Jumbotron(
    [
     html.Center([
         html.Img(src="https://upload.wikimedia.org/wikipedia/commons/7/73/Logo_kementerian_keuangan_republik_indonesia.png", style=dict(width=150)),   
         html.H1("Debt Sustainability Analytics", className="display-3"),
         html.P(
            "Analisis atas kesinambungan utang publik",
            className="lead",
            ),
         html.Hr(className="my-2"),
         html.P(
            "Mengacu pada Framework DSA IMF 2013"
            ),
         html.P(html.A(dbc.Button("Get Started", color="primary"), href='/baseline-scenario'), className="lead"),         
         ])

    ])

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
