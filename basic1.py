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
detail = df
projections_debt_creating_flows = df[df['Tahun']>=2021]
cumulative_projection = projections_debt_creating_flows.sum(axis=0)

x = df['Tahun']

debt_creating_flows = go.Figure()
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Primary deficit'], name='Primary Deficit'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Real GDP growth'], name='Real GDP Growth'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Real interest rate'], name='Real Interest Rate'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Exchange rate depreciation'], name='Exchange Rate Depreciation'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Other debt-creating flows'], name='Other Debt-Creating Flows'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Residual'], name='Residual'))
debt_creating_flows.add_trace(go.Scatter(x=x, y=df['Change in gross public sector debt'],
                    mode='lines+markers',
                    name='Change in gross public sector debt', line=dict(color='firebrick', width=4)))

debt_creating_flows.add_annotation(x=2022, y=9,
            text="Projections--->",showarrow=False)

debt_creating_flows.update_layout(barmode='relative',
                                  height=600, 
                                  colorway=px.colors.qualitative.Vivid, 
                                  title=dict(
                                      text="Debt-Creating Flows (in Percent of GDP)",
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
                                      t=90,
                                      pad=4))

debt_creating_flows.update_xaxes(showgrid=False)

debt_creating_flows.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

primary_deficit = go.Figure()

primary_deficit.add_trace(go.Scatter(x=x, y=df['Primary deficit'],
                    mode='lines+markers',
                    name='Primary deficit', line=dict(color='mediumslateblue', width=4)))

primary_deficit.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

primary_deficit.update_xaxes(showgrid=False)

primary_deficit.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

primary_revenue = go.Figure()

primary_revenue.add_trace(go.Scatter(x=x, y=df['Primary (noninterest) revenue and grants'],
                    mode='lines+markers',
                    name='Primary (noninterest) revenue and grants', line=dict(color='mediumslateblue', width=4)))

primary_revenue.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

primary_revenue.update_xaxes(showgrid=False)

primary_revenue.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

primary_expenditure = go.Figure()

primary_expenditure.add_trace(go.Scatter(x=x, y=df['Primary (noninterest) expenditure'],
                    mode='lines+markers',
                    name='Primary (noninterest) expenditure', line=dict(color='mediumslateblue', width=4)))

primary_expenditure.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

primary_expenditure.update_xaxes(showgrid=False)

primary_expenditure.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

real_interest_rate = go.Figure()

real_interest_rate.add_trace(go.Scatter(x=x, y=df['Real interest rate'],
                    mode='lines+markers',
                    name='Real interest rate', line=dict(color='lightseagreen', width=4)))

real_interest_rate.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

real_interest_rate.update_xaxes(showgrid=False)

real_interest_rate.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

real_gdp_growth = go.Figure()

real_gdp_growth.add_trace(go.Scatter(x=x, y=df['Real GDP growth'],
                    mode='lines+markers',
                    name='Real GDP growth', line=dict(color='lightseagreen', width=4)))

real_gdp_growth.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

real_gdp_growth.update_xaxes(showgrid=False)

real_gdp_growth.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

exchange_rate_depreciation = go.Figure()

exchange_rate_depreciation.add_trace(go.Scatter(x=x, y=df['Identified debt-creating flows'],
                    mode='lines+markers',
                    name='Exchange Rate Depreciation', line=dict(color='lightseagreen', width=4)))

exchange_rate_depreciation.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

exchange_rate_depreciation.update_xaxes(showgrid=False)

exchange_rate_depreciation.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

increase_financing_needs = go.Figure()

increase_financing_needs.add_trace(go.Scatter(x=x, y=df['Primary (noninterest) expenditure'],
                    mode='lines+markers',
                    name='Other increases in financing needs', line=dict(color='deepskyblue', width=4)))

increase_financing_needs.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

increase_financing_needs.update_xaxes(showgrid=False)

increase_financing_needs.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

contingent_liabilities = go.Figure()

contingent_liabilities.add_trace(go.Scatter(x=x, y=df['Primary deficit'],
                    mode='lines+markers',
                    name='Recognition of implicit or contingent liabilities', line=dict(color='deepskyblue', width=4)))

contingent_liabilities.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

contingent_liabilities.update_xaxes(showgrid=False)

contingent_liabilities.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

decrease_financing_needs = go.Figure()

decrease_financing_needs.add_trace(go.Scatter(x=x, y=df['Primary (noninterest) revenue and grants'],
                    mode='lines+markers',
                    name='Other increases in financing needs', line=dict(color='deepskyblue', width=4)))

decrease_financing_needs.update_layout(
    height=250,
    title=dict(
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1
        ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
        ),
    margin=dict(
        l=0,
        r=0,
        b=20,
        t=20,
        pad=4))

decrease_financing_needs.update_xaxes(showgrid=False)

decrease_financing_needs.add_vrect(
    x0="2021", x1="2027",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

CONTRIBUTION_TO_CHANGES_IN_PUBLIC_DEBT_DETAIL = [
    dbc.CardHeader(html.H5("Contribution to Changes in Public Debt")),
    dbc.CardBody(
        [
            dcc.Graph(figure=debt_creating_flows),
            dbc.Card([
                dbc.CardHeader(html.Center(html.H4("Identified debt-creating flows"))),
                dbc.CardBody([
                    html.Center(html.H5("Primary Deficit")),
                    #primary deficit
            dbc.Row([
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H5("Primary Deficit (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=primary_deficit)
                                     ])   
                            ]
                        )]
                    ,md=4),
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H5("Primary Revenue (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=primary_revenue)
                                     ])   
                            ]
                        )]
                    ,md=4),
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H5("Primary Expenditure (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=primary_expenditure)
                                     ])   
                            ]
                        )]
                    ,md=4),
                ],
                    style={"marginTop": 30}),
            html.P(""),
            html.Center(html.H5("Automatic debt dynamics")),
            #automatic debt dynamics
            dbc.Row([
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H5("Real Interest Rate (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=real_interest_rate)
                                     ])   
                            ]
                        )]
                    ,md=4),
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H5("Real GDP Growth (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=real_gdp_growth)
                                     ])   
                            ]
                        )]
                    ,md=4),
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H6("Exchange Rate Depreciation (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=exchange_rate_depreciation)
                                     ])   
                            ]
                        )]
                    ,md=4),
                ],
                    style={"marginTop": 30}),
            html.P(""),
            html.Center(html.H5("Other identified debt-creating flows")),
            #other identified debt-creating flows
            dbc.Row([
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H6("Other Inc. Financing Needs (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=increase_financing_needs)
                                     ])   
                            ]
                        )]
                    ,md=4),
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H5("Contingent Liabilities (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=contingent_liabilities)
                                     ])   
                            ]
                        )]
                    ,md=4),
                dbc.Col(
                    [dbc.Card(
                        [dbc.CardHeader(
                            html.H6("Other Dec. Financing Needs (%GDP)")
                            ),
                         dbc.CardBody([
                             dcc.Graph(figure=decrease_financing_needs)
                                     ])   
                            ]
                        )]
                    ,md=4),
                ],
                    style={"marginTop": 30})
                    
                    ])
                               
                    ])
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
