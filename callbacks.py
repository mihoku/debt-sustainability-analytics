from dash.dependencies import Input, Output
import pathlib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from app import app
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data-source").resolve()
MAP_PATH = PATH.joinpath("other-datasets").resolve()

projection_benchmark = pd.read_csv(DATA_PATH.joinpath('forecast-error-benchmark.csv'),low_memory=False, sep=";", header=0)
forecast_history = pd.read_csv(DATA_PATH.joinpath('forecast-error-track-record.csv'),low_memory=False, sep=";", header=0)

@app.callback(
    Output('primary-balance-projection-track-record', 'figure'),
    Output('inflation-projection-track-record', 'figure'),
    Output('gdp-growth-projection-track-record', 'figure'),
    Input('forecast-comparator-group', 'value')
)

def update_graph_projection_track_record(group):
    
    benchmark = projection_benchmark[projection_benchmark['Category']==group]
    benchmark_gdp = benchmark[benchmark['Indicator']=='Growth']
    benchmark_inflation = benchmark[benchmark['Indicator']=='Inflation']
    benchmark_pb = benchmark[benchmark['Indicator']=='Primary Balance']
    
    chart_GDP = go.Figure()
    
    chart_GDP.add_trace(go.Scatter(x=benchmark_gdp['Tahun'], y=benchmark_gdp['25th'],
                                   fill=None,
                                   mode='lines',
                                   name='forecast errors',
                                   line=dict(width=0.5, color='rgb(111, 231, 219)'),
                                   ))
    
    chart_GDP.add_trace(go.Scatter(
        x=benchmark_gdp['Tahun'], y=benchmark_gdp['75th'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        name='Interquartile range (25-75):',
        fill='tonexty'
        ))
    
    chart_GDP.add_trace(go.Scatter(
        x=benchmark_gdp['Tahun'], y=benchmark_gdp['Median'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=3, color='#000'),
        name='Median'))
    
    chart_GDP.add_trace(go.Scatter(
        x=forecast_history['Tahun'], y=forecast_history['Growth-Forecast-Error'],
        hoverinfo='x+y',
        mode='markers',
        line=dict(width=8, color='firebrick'),
        name='Indonesia Forecast Error'))
    
    chart_GDP.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4)
    )
    
    
    chart_Inflation = go.Figure()
    
    chart_Inflation.add_trace(go.Scatter(x=benchmark_inflation['Tahun'], y=benchmark_inflation['25th'],
                                   fill=None,
                                   mode='lines',
                                   line=dict(width=0.5, color='rgb(111, 231, 219)'),
                                   name='forecast errors'
                                   ))
    
    chart_Inflation.add_trace(go.Scatter(
        x=benchmark_inflation['Tahun'], y=benchmark_inflation['75th'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        name='Interquartile range (25-75):',
        fill='tonexty'
        ))    
    
    chart_Inflation.add_trace(go.Scatter(
        x=benchmark_inflation['Tahun'], y=benchmark_inflation['Median'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=3, color='#000'),
        name='Median'))
    
    chart_Inflation.add_trace(go.Scatter(
        x=forecast_history['Tahun'], y=forecast_history['Inflation-Forecast-Error'],
        hoverinfo='x+y',
        mode='markers',
        line=dict(width=8, color='firebrick'),
        name='Indonesia Forecast Error'))
    
    chart_Inflation.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4))
    
    chart_PB = go.Figure()
    
    chart_PB.add_trace(go.Scatter(x=benchmark_pb['Tahun'], y=benchmark_pb['25th'],
                                   fill=None,
                                   mode='lines',
                                   line=dict(width=0.5, color='rgb(111, 231, 219)'),
                                   name='forecast errors'
                                   ))
    
    chart_PB.add_trace(go.Scatter(
        x=benchmark_pb['Tahun'], y=benchmark_pb['75th'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        name='Interquartile range (25-75):',
        fill='tonexty'
        ))
    
    chart_PB.add_trace(go.Scatter(
        x=benchmark_pb['Tahun'], y=benchmark_pb['Median'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=3, color='#000'),
        name='Median'))
    
    chart_PB.add_trace(go.Scatter(
        x=forecast_history['Tahun'], y=forecast_history['PB-Forecast-Error'],
        hoverinfo='x+y',
        mode='markers',
        line=dict(width=8, color='firebrick'),
        name='Indonesia Forecast Error'))
    
    chart_PB.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ),
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=4))
    
    return chart_PB, chart_Inflation, chart_GDP