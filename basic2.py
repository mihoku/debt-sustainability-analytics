import dash
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

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data-source").resolve()
OTHER_PATH = PATH.joinpath("other-datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath('debt maturity.csv'),low_memory=False, sep=";", header=0)
x = df['Tahun']

composition_of_public_debt = go.Figure()
composition_of_public_debt.add_trace(go.Scatter(
    x=x, y=df['Short Term'],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.2, color='rgb(250, 0, 0)'),
    stackgroup='one', # define stack group
    name='Short Term'
))
composition_of_public_debt.add_trace(go.Scatter(
    x=x, y=df['Long Term'],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.2, color='rgb(37, 47, 255)'),
    stackgroup='one',
    name='Long Term'
))

composition_of_public_debt.show()

composition_of_public_debt.add_vrect(
    x0="2021", x1="2026",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

composition_of_public_debt.add_annotation(x=2020, y=100,
            text="Projections--->",showarrow=False)

composition_of_public_debt.update_layout(yaxis_range=(0, 140))
composition_of_public_debt.update_layout(width=800, height=500)
composition_of_public_debt.update_layout(barmode='relative', 
                                  colorway=px.colors.qualitative.Vivid, 
                                  title=dict(
                                      text="Composition of Public Debt by Maturity (in Percent of GDP)",
                                      pad_t=30,
                                      pad_b=50,
                                      yanchor="top",
                                      y=1
                                      ),
                                  legend=dict(
                                      orientation="h",
                                      yanchor="bottom",
                                      y=1.02,
                                      xanchor="right",
                                      x=1
                                      ),
                                  margin=dict(
                                      l=30,
                                      r=30,
                                      b=50,
                                      t=90,
                                      pad=2))

BASIC2 = dbc.Container(
    [
        dbc.Row([dbc.Col(dcc.Graph(figure = composition_of_public_debt), md=12),], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card()),], style={"marginTop": 30}),
    ],
    className="mt-12",
)