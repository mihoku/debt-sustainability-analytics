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
df2 = pd.read_csv(DATA_PATH.joinpath('debt currency.csv'),low_memory=False, sep=";", header=0)
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
composition_of_public_debt.update_layout(height=500)
composition_of_public_debt.update_layout(barmode='relative', 
                                  colorway=px.colors.qualitative.Vivid, 
                                  title=dict(
                                      text="By Maturity (in Percent of GDP)",
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
                                      l=30,
                                      r=30,
                                      b=50,
                                      t=50,
                                      pad=2))

composition_of_public_debt_by_currency = go.Figure()
composition_of_public_debt_by_currency.add_trace(go.Scatter(
    x=x, y=df2['Local'],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.2, color='rgb(255, 140, 0)'),
    stackgroup='one', # define stack group
    name='Local Currency'
))
composition_of_public_debt_by_currency.add_trace(go.Scatter(
    x=x, y=df2['Foreign'],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.2, color='rgb(0,128, 0)'),
    stackgroup='one',
    name='Foreign Currency'
))


composition_of_public_debt_by_currency.add_vrect(
    x0="2021", x1="2026",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

composition_of_public_debt_by_currency.add_annotation(x=2020, y=100,
            text="Projections--->",showarrow=False)

composition_of_public_debt_by_currency.update_layout(yaxis_range=(0, 140))
composition_of_public_debt_by_currency.update_layout(height=500)
composition_of_public_debt_by_currency.update_layout(barmode='relative', 
                                  colorway=px.colors.qualitative.Vivid, 
                                  title=dict(
                                      text="By Currency (in Percent of GDP)",
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
                                      l=30,
                                      r=30,
                                      b=50,
                                      t=50,
                                      pad=2))

##########gross debt

gross_debt_data = pd.read_csv(DATA_PATH.joinpath('gross nominal debt.csv'),low_memory=False, sep=";", header=0)
year = gross_debt_data['Tahun']

baseline = gross_debt_data['Baseline']
debt = gross_debt_data['Debt']
primary_balance = gross_debt_data['Primary Balance']
historical = gross_debt_data['Historical']

gross_debt = go.Figure()
# Create and style traces
gross_debt.add_trace(go.Scatter(x=year, y=baseline, name='Baseline',
                         line=dict(color='royalblue', width=2)))
gross_debt.add_trace(go.Scatter(x=year, y=debt, name = 'Debt (in Percent of GDP)',
                         line=dict(color='darkgray', width=2)))
gross_debt.add_trace(go.Scatter(x=year, y=primary_balance, name='Primary Balance',
                         line=dict(color='darkmagenta', width=2, dash='dash')))
gross_debt.add_trace(go.Scatter(x=year, y=historical, name='Historical',
                         line = dict(color='black', width=2, dash='dot')))

gross_debt.update_layout(yaxis_range=(0, 160))
gross_debt.update_layout(xaxis_range=(2019, 2026))
gross_debt.update_layout(height=500)
gross_debt.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ),
    title=dict(
        text="Gross Nominal Public Debt (in percent of GDP)",
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=90,
        pad=2))

gross_debt.update_traces(mode='lines')

gross_debt.add_vrect(
    x0="2021", x1="2026",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

gross_debt.add_annotation(x=2020, y=50,
            text="Projections--->",showarrow=False)

##########gross financing need

financing_need_data = pd.read_csv(DATA_PATH.joinpath('financing need.csv'),low_memory=False, sep=";", header=0)
year = financing_need_data['Tahun']

baseline = financing_need_data['Baseline']
primary_balance = financing_need_data['Primary Balance']
historical = financing_need_data['Historical']

financing_need = go.Figure()
# Create and style traces
financing_need.add_trace(go.Scatter(x=year, y=baseline, name='Baseline',
                         line=dict(color='royalblue', width=2)))
financing_need.add_trace(go.Scatter(x=year, y=primary_balance, name='Primary Balance',
                         line=dict(color='darkmagenta', width=2, dash='dash')))
financing_need.add_trace(go.Scatter(x=year, y=historical, name='Historical',
                         line = dict(color='black', width=2, dash='dot')))

financing_need.update_layout(yaxis_range=(0, 35))
financing_need.update_layout(xaxis_range=(2019, 2026))
financing_need.update_layout(height=500)
financing_need.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ),
    title=dict(
        text="Public Gross Financing Needs (in percent of GDP)",
        pad_t=0,
        pad_b=50,
        yanchor="top",
        y=1),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=90,
        pad=2))

financing_need.update_traces(mode='lines')

financing_need.add_vrect(
    x0="2021", x1="2026",
    fillcolor="#888",
    opacity=0.2, line_width=0
)

financing_need.add_annotation(x=2020, y=10,
            text="Projections--->",showarrow=False)

BASIC2 = dbc.Container([
        dbc.Card(
        [
            dbc.CardHeader(html.Center(html.H4("Composition of Public Debt"))),
            dbc.CardBody([
                dbc.Row([dbc.Col(dcc.Graph(figure = composition_of_public_debt), md=6),dbc.Col(dcc.Graph(figure = composition_of_public_debt_by_currency), md=6)], style={"marginTop": 30}),
                dbc.Row([dbc.Col(dbc.Card()),], style={"marginTop": 30}),])
            ]),
        dbc.Card(
            [
                dbc.CardHeader(html.Center(html.H4("Alternative Scenarios"))),
                dbc.CardBody([
                    dbc.Row([dbc.Col(dcc.Graph(figure = gross_debt), md=6),dbc.Col(dcc.Graph(figure = financing_need), md=6)], style={"marginTop": 30}),
                    dbc.Row([dbc.Col(dbc.Card()),], style={"marginTop": 30}),])
                ])],
    className="mt-12", style={"marginTop": 50,"marginBottom": 50}
)