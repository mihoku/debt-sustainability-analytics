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

df = pd.read_csv(DATA_PATH.joinpath('change in debt.csv'),low_memory=False, sep=";", header=0)
x = df['Tahun']

projection_benchmark = pd.read_csv(DATA_PATH.joinpath('forecast-error-benchmark.csv'),low_memory=False, sep=";", header=0)
comparator_group = projection_benchmark['Category'].unique()

median_and_percentile_rank = pd.read_csv(DATA_PATH.joinpath('median-and-percentile-rank-of-projection-error.csv'),low_memory=False, sep=";", header=0)

GROWTH = [
    dbc.CardHeader(html.H5("Real GDP Growth Forecast Track Record")),
    dbc.CardBody(
        [
            dcc.Graph(id='gdp-growth-projection-track-record')
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

INFLATION = [
    dbc.CardHeader(html.H5("Inflation (Deflator) Forecast Track Record")),
    dbc.CardBody(
        [
            dcc.Graph(id='inflation-projection-track-record')
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

PRIMARY_BALANCE = [
    dbc.CardHeader(html.H5("Primary Balance Forecast Track Record")),
    dbc.CardBody(
        [
            dcc.Graph(id='primary-balance-projection-track-record')
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

REALISM = dbc.Container(
    [
     dbc.Row(
         [
             dbc.Col(
                 dbc.Card(children=[
                     dbc.CardHeader(html.H5("Forecast Track Record, Compared to Other Countries")),
                     dbc.CardBody(children=[
                         html.P("Pilih Kelompok Negara sebagai Pembanding"),
                         dcc.Dropdown(
                             options=[{'label': i, 'value':i} for i in comparator_group],
                             value='all countries',
                             id='forecast-comparator-group'
                             ),
                         html.P(""),
                         html.P("Analisis ini menilai track record dalam memproyeksikan variabel makroekonomi kunci (meliputi pertumbuhan GDP riil, keseimbangan primer, dan inflasi) secara relatif terhadap track record dari negara-negara lain."),
                         html.P(""),
                         html.P("Analisis juga menyajikan 2 (dua) summary statistics yang meliputi median forecast error dan percentile rank dari median forecast error tersebut dibandingkan negara lain yang termasuk Market Access Country (MAC)."),
                         dash_table.DataTable(
                             id='median-and-percentile-rank',
                             columns=[{"name": str(i), "id": str(i)} for i in median_and_percentile_rank.columns],
                             data=median_and_percentile_rank.to_dict('records'),
                             style_cell={'fontSize':12, 'font-family':'sans-serif'}
                             )
                         ])  
                     ])
                     ,md=6),
             dbc.Col(dbc.Card(GROWTH),md=6)
          ], style={"marginTop": 50,"marginBottom": 50}),
     dbc.Row(
         [
             dbc.Col(dbc.Card(PRIMARY_BALANCE),md=6),
             dbc.Col(dbc.Card(INFLATION),md=6)
          ], style={"marginTop": 50,"marginBottom": 50})
    ],
    className="mt-12",
)