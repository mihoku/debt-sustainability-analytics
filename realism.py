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

capb_data = pd.read_csv(DATA_PATH.joinpath('capb-data.csv'),low_memory=False, sep=";", header=0)

capb_adjustment = capb_data[capb_data['CAPB']=='3-year adjustment']
capb_adjustment_top_quartile_marker = capb_adjustment[capb_adjustment['Bin']=='3.5']
capb_adjustment_top_quartile = capb_adjustment[capb_adjustment['Category']>=capb_adjustment_top_quartile_marker.iloc[0]['Category']]
capb_adjustment_non_top_quartile = capb_adjustment[capb_adjustment['Category']<capb_adjustment_top_quartile_marker.iloc[0]['Category']]

capb_average = capb_data[capb_data['CAPB']=='3-year average level']
capb_average_top_quartile_marker = capb_average[capb_average['Bin']=='4']
capb_average_top_quartile = capb_average[capb_average['Category']>=capb_average_top_quartile_marker.iloc[0]['Category']]
capb_average_non_top_quartile = capb_average[capb_average['Category']<capb_average_top_quartile_marker.iloc[0]['Category']]

categorical_order_adjustment = capb_adjustment['Bin'].tolist()
categorical_order_average = capb_average['Bin'].tolist()

capb_figure_adjustment = go.Figure()
capb_figure_adjustment.add_trace(go.Bar(x=capb_adjustment_non_top_quartile['Bin'], y=capb_adjustment_non_top_quartile['Frequency'], name='Distribution'))
capb_figure_adjustment.add_trace(go.Bar(x=capb_adjustment_top_quartile['Bin'], y=capb_adjustment_top_quartile['Frequency'], name='3-year CAPB adjustment > 3% of GDP in approx. top quartile'))
capb_figure_adjustment.update_xaxes(categoryorder='array', categoryarray=categorical_order_adjustment)
capb_figure_adjustment.update_layout(barmode='relative',
                                  colorway=px.colors.qualitative.Vivid, 
                                  title=dict(
                                      text="3-year Adjustment in Cyclically-Adjusted Primary Balance",
                                      pad_t=0,
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
                                      l=0,
                                      r=0,
                                      b=50,
                                      t=50,
                                      pad=4))

capb_figure_average = go.Figure()
capb_figure_average.add_trace(go.Bar(x=capb_average_non_top_quartile['Bin'], y=capb_average_non_top_quartile['Frequency'], name='Distribution'))
capb_figure_average.add_trace(go.Bar(x=capb_average_top_quartile['Bin'], y=capb_average_top_quartile['Frequency'], name='3-year avg CAPB level > 3.5% of GDP in approx. top quartile'))
capb_figure_average.update_xaxes(categoryorder='array', categoryarray=categorical_order_average)
capb_figure_average.update_layout(barmode='relative',
                                  colorway=px.colors.qualitative.Vivid, 
                                  title=dict(
                                      text="3-year Average Level of Cyclically-Adjusted Primary Balance",
                                      pad_t=0,
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
                                      l=0,
                                      r=0,
                                      b=50,
                                      t=50,
                                      pad=4))

GROWTH = dbc.Card([
    dbc.CardHeader(html.H5("Real GDP Growth Forecast Track Record")),
    dbc.CardBody(
        [
            dcc.Graph(id='gdp-growth-projection-track-record')
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
])

INFLATION = dbc.Card([
    dbc.CardHeader(html.H5("Inflation (Deflator) Forecast Track Record")),
    dbc.CardBody(
        [
            dcc.Graph(id='inflation-projection-track-record')
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
])

PRIMARY_BALANCE = dbc.Card([
    dbc.CardHeader(html.H5("Primary Balance Forecast Track Record")),
    dbc.CardBody(
        [
            dcc.Graph(id='primary-balance-projection-track-record')
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]),

CAPB = dbc.Card([
    dbc.CardHeader(html.Center(html.H5("Assessing the Realism of Projected Fiscal Adjustment"))),
    dbc.CardBody(dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=capb_figure_adjustment),md=6),
            dbc.Col(dcc.Graph(figure=capb_figure_average),md=6)
            ]
        ),
        style={"marginTop": 0, "marginBottom": 0},
    ),
])

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
             dbc.Col(GROWTH,md=6)
          ], style={"marginTop": 50,"marginBottom": 50}),
     dbc.Row(
         [
             dbc.Col(PRIMARY_BALANCE,md=6),
             dbc.Col(INFLATION,md=6)
          ], style={"marginTop": 50,"marginBottom": 50}),
     dbc.Row(dbc.Col(CAPB,md=12), style={"marginTop": 50,"marginBottom": 50})
    ],
    className="mt-12",
)