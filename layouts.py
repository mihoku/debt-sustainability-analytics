import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
import dash_table
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
public_debt_contributor_header = ['No','Components']
public_debt_contributor_header = public_debt_contributor_header+np.arange(x.min(), x.max()+1).tolist()

public_debt_contributor = df.set_index('Tahun').T.rename_axis('Components').rename_axis(0).reset_index()

projection_benchmark = pd.read_csv(DATA_PATH.joinpath('forecast-error-benchmark.csv'),low_memory=False, sep=";", header=0)
comparator_group = projection_benchmark['Category'].unique()

median_and_percentile_rank = pd.read_csv(DATA_PATH.joinpath('median-and-percentile-rank-of-projection-error.csv'),low_memory=False, sep=";", header=0)

fig = go.Figure()
fig.add_trace(go.Bar(x=x, y=df['Primary deficit'], name='Primary Deficit'))
fig.add_trace(go.Bar(x=x, y=df['Real GDP growth'], name='Real GDP Growth'))
fig.add_trace(go.Bar(x=x, y=df['Real interest rate'], name='Real Interest Rate'))
fig.add_trace(go.Bar(x=x, y=df['Exchange rate depreciation'], name='Exchange Rate Depreciation'))
fig.add_trace(go.Bar(x=x, y=df['Other debt-creating flows'], name='Other Debt-Creating Flows'))
fig.add_trace(go.Bar(x=x, y=df['Residual'], name='Residual'))
fig.add_trace(go.Scatter(x=x, y=df['Change in gross public sector debt'],
                    mode='lines+markers',
                    name='Change in gross public sector debt', line=dict(color='firebrick', width=4)))

fig.update_layout(barmode='relative',height=600, colorway=px.colors.qualitative.Vivid, title_text="Debt-Creating Flows (in Percent of GDP)")

fig.update_xaxes(showgrid=False)

fig.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0,
)

CONTRIBUTION_TO_CHANGES_IN_PUBLIC_DEBT_DETAIL = [
    dbc.CardHeader(html.H5("Contribution to Changes in Public Debt")),
    dbc.CardBody(
        [
            dcc.Graph(figure=fig),
            dash_table.DataTable(
               id='ctcipd',
               columns=[{"name": str(i), "id": str(i)} for i in public_debt_contributor.columns],
               data=public_debt_contributor.to_dict('records'),
               style_cell={'fontSize':10, 'font-family':'sans-serif'}
               )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

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
     
BASIC1 = dbc.Container(
    [
     dbc.Row([dbc.Col(dbc.Card(CONTRIBUTION_TO_CHANGES_IN_PUBLIC_DEBT_DETAIL),md=12)], style={"marginTop": 50,"marginBottom": 50}),   
    ],
    className="mt-12",
)

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
