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

df1 = pd.read_csv(DATA_PATH.joinpath('Stress-test.csv'),low_memory=False, sep=",", header=0)

STRESS_TEST = dbc.Container([
    #row untuk main content
    dbc.Row([
        #kolom untuk menu skenario
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H6("Primary Balance Shock Scenario")
                        ),
                    dbc.CardBody([
                        html.Strong(html.P("Impact on Revenue")),
                        dcc.Dropdown(
                            id='impact-on-revenue-pb',
                            options=[
                                {'label': 'Shock bersumber dari belanja saja', 'value': 'Belanja'},
                                {'label': 'Shock bersumber dari belanja dan pendapatan', 'value': 'BelanjaPendapatan'},
                                ],
                            value='Belanja'
                            ),
                        html.P(""),
                        html.Strong(html.P("Interest Rate Shock")),
                        html.P("Penurunan Primary Balance sebesar 1% GDP berdampak pada peningkatan tingkat suku bunga sebesar 25 bps."),                
                        html.P("",id="pb_interest_rate_shock"),
                        html.P(""),
                        html.Strong(html.P("Size of Primary Balance Shock")),
                        html.P("Porsi konsolidasi fiskal yang tidak terrealisasi"),
                        dcc.Slider(
                            id="size-of-pb-shock",
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            marks={
                                0: '0%',
                                1: '100%'
                                },
                            ),
                        html.Div(id='pb-shock-size-container'),
                        html.P(""),
                        html.Strong(html.P("Based on Planned Adjustment")),
                        html.Div(id='cumulative_pb_shock_impact_adjustment_scenario'),
                        html.P(""),
                        html.Strong(html.P("Based on 10Y historical std. dev.")),
                        html.Div(id='cumulative_pb_shock_impact_10y_stdev'),
                        ]
                        )
                    ]
                ),
            
            ],md=5),
        #kolom untuk grafik hasil stress tests
        dbc.Col([
            
                 dbc.Row(
                     [
                         dbc.Col(
                             dbc.Card(children=[
                                 dbc.CardHeader(html.H5("Macro-Fiscal Stress Tests")),
                                 dbc.CardBody(
                                     [
                                         dbc.Row(dbc.Col(dcc.Graph(id="Gross_Nominal_Public_Debt_Percent_GDP_Macro_Fiscal"),md=12),style={'marginTop':30, 'marginBottom':30}),
                                         dbc.Row(dbc.Col(dcc.Graph(id="Gross_Nominal_Public_Debt_Percent_Revenue_Macro_Fiscal"),md=12),style={'marginTop':30, 'marginBottom':30}),
                                         dbc.Row(dbc.Col(dcc.Graph(id="Gross_Financing_Need_Macro_Fiscal"),md=12),style={'marginTop':30, 'marginBottom':30})
                                         ])]
                                 
                                 ))]),
                 dbc.Row(
                     [
                         dbc.Col(
                             dbc.Card(children=[
                                 dbc.CardHeader(html.H5("Additional Stress Tests")),
                                 dbc.CardBody(
                                     [
                                         dbc.Row(dbc.Col(dcc.Graph(id="Gross_Nominal_Public_Debt_Percent_GDP_Additional"),md=12),style={'marginTop':30, 'marginBottom':30}),
                                         dbc.Row(dbc.Col(dcc.Graph(id="Gross_Nominal_Public_Debt_Percent_Revenue_Additional"),md=12),style={'marginTop':30, 'marginBottom':30}),
                                         dbc.Row(dbc.Col(dcc.Graph(id="Gross_Financing_Need_Percent_GDP_Additional"),md=12),style={'marginTop':30, 'marginBottom':30})
                                         ])]
                                 
                                 ,style={'marginTop':30, 'marginBottom':50}),
            
                        )]
         
                )
            
            ],md=7)
        ])
    ]
    ,style={'marginTop':50, 'marginBottom':50})



