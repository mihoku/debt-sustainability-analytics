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
from datetime import date

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data-source").resolve()
OTHER_PATH = PATH.joinpath("other-datasets").resolve()

heatmap_data = [[.5, 1, .5, 1, 1],
        [.5, 0, .5, 1, .5],
        [.5, 1, .5, .5, 0]]

debt_profile_data = pd.read_csv(DATA_PATH.joinpath('debt-profile-benchmark-and-data.csv'),low_memory=False, sep=";", header=0)
debt_profile_data['y'] = 100*debt_profile_data['t-1']/debt_profile_data['Full']
debt_profile_data['bar_width'] = 0.8
max_point = round(debt_profile_data['y'].max()*1.2,0)

debt_risk=['Real GDP Growth Shock','Primary Balance Shock','Real Interest Rate Shock','Exchange Rate Shock','Contingent Liability shock']

heatmap_risk = go.Figure(data=go.Heatmap(
                    z=heatmap_data,
                    colorscale=[[0, 'green'],[0.5, 'orange'],[1, 'firebrick']]))

#add bar name below
heatmap_risk.add_annotation(x=0, y=0,
                              xanchor='center', yanchor='top',
                              text=debt_profile_data.iloc[0]['Name'],
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)


heatmap_risk.add_annotation(x=1, y=0.2,
                              xanchor='center', yanchor='top',
                              text='External Financing',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)
heatmap_risk.add_annotation(x=1, y=0,
                              xanchor='center', yanchor='top',
                              text='Requirement',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)

heatmap_risk.add_annotation(x=2, y=0.4,
                              xanchor='center', yanchor='top',
                              text="Annual Change",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)
heatmap_risk.add_annotation(x=2, y=0.2,
                              xanchor='center', yanchor='top',
                              text="in Short-Term",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)
heatmap_risk.add_annotation(x=2, y=0,
                              xanchor='center', yanchor='top',
                              text="Public Debt",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)

heatmap_risk.add_annotation(x=3, y=0.2,
                              xanchor='center', yanchor='top',
                              text='Public Debt Held',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)
heatmap_risk.add_annotation(x=3, y=0,
                              xanchor='center', yanchor='top',
                              text='by Non-Residents',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)

heatmap_risk.add_annotation(x=4, y=0.2,
                              xanchor='center', yanchor='top',
                              text='Public Debt',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)
heatmap_risk.add_annotation(x=4, y=0,
                              xanchor='center', yanchor='top',
                              text='in Foreign Currency',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)

for x in range(0,5):
    for y in range(0,2):
        heatmap_risk.add_annotation(x=x, y=y+1,
                              xanchor='center', yanchor='top',
                              text=debt_risk[x],
                              font=dict(family='Arial',
                                        size=14,
                                        color='#fff'),
                              showarrow=False)

for i in range(0,5):
    for j in range(0,3):    
        #rectangles
        heatmap_risk.add_trace(go.Scatter(x=[i-.5,i-.5,i+.5,i+.5,i-.5], y=[j-.5,j+.5,j+.5,j-.5,j-.5], mode='lines',
                                          line=dict(color='black', width=2),
                                          connectgaps=True, hovertemplate=''
                                          ))

heatmap_risk.add_annotation(y=0, x=-0.5,
                              xanchor='right',
                              text='Debt Profile',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

heatmap_risk.add_annotation(y=1, x=-0.5,
                              xanchor='right',
                              text='Gross Financing Needs',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

heatmap_risk.add_annotation(y=2, x=-0.5,
                              xanchor='right',
                              text='Debt Level',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

heatmap_risk.update_layout(
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
#    autosize=False,
    margin=dict(
#        autoexpand=False,
        l=0,
        r=0,
        t=0,
        b=0
    ),
    showlegend=False,
    plot_bgcolor='white',
    hovermode=False
)

########################debt profile vulnerabilities

debt_profile_vuln = go.Figure()

debt_profile_vuln.add_trace(go.Scatter(x=[0], y=[max_point], mode='markers',
        name='',
        line=dict(color='white', width=1),
        connectgaps=True, hovertemplate=''
    ))

for i in range(0,5):
    
#    debt_profile_vuln.add_vrect(
#        x0=debt_profile_data.iloc[i]['x']-1, x1=debt_profile_data.iloc[i]['x']+1,line_width=2
#        )
    
    #rectangles
    debt_profile_vuln.add_trace(go.Scatter(x=[debt_profile_data.iloc[i]['x']-1,debt_profile_data.iloc[i]['x']-1,debt_profile_data.iloc[i]['x']+1,debt_profile_data.iloc[i]['x']+1,debt_profile_data.iloc[i]['x']-1], y=[0,max_point,max_point,0,0], mode='lines',
        line=dict(color='black', width=2),
        connectgaps=True, hovertemplate=''
    ))
    
    #lower early warning
    debt_profile_vuln.add_trace(go.Scatter(x=[debt_profile_data.iloc[i]['x']-1,debt_profile_data.iloc[i]['x'],debt_profile_data.iloc[i]['x']+1], y=[25,25,25], mode='lines',
        name=debt_profile_data.iloc[i]['25'],
        line=dict(color='mediumslateblue', dash='dash', width=2),
        connectgaps=True, hovertemplate=''
    ))
    
    #upper early warning
    debt_profile_vuln.add_trace(go.Scatter(x=[debt_profile_data.iloc[i]['x']-1,debt_profile_data.iloc[i]['x'],debt_profile_data.iloc[i]['x']+1], y=[75,75,75], mode='lines',
        name=str(debt_profile_data.iloc[i]['75']),
        line=dict(color='black', dash='dash', width=2),
        connectgaps=True, hovertemplate=''
    ))
    
    # labeling the left_side of the plot 25
    debt_profile_vuln.add_annotation(x=debt_profile_data.iloc[i]['x']-1, y=25,
                                  xanchor='right', yanchor='middle',
                                  text='{}'.format(round(debt_profile_data.iloc[i]['25'],2)),
                                  font=dict(family='Arial',
                                            size=12),
                                  showarrow=False)
    # labeling the left_side of the plot 75
    debt_profile_vuln.add_annotation(x=debt_profile_data.iloc[i]['x']-1, y=75,
                                  xanchor='right', yanchor='middle',
                                  text='{}'.format(round(debt_profile_data.iloc[i]['75'],2)),
                                  font=dict(family='Arial',
                                            size=12),
                                  showarrow=False)
    # labeling the plot data
    debt_profile_vuln.add_annotation(x=debt_profile_data.iloc[i]['x'], y=debt_profile_data.iloc[i]['y']+10,
                                  xanchor='center', yanchor='middle',
                                  text='{} {}'.format(round(debt_profile_data.iloc[i]['t-1'],2),debt_profile_data.iloc[i]['satuan']),
                                  font=dict(family='Arial',
                                            size=14),
                                  showarrow=False)


debt_profile_vuln.add_trace(go.Bar(x=debt_profile_data['x'], 
                                   y=debt_profile_data['y'], 
                                   width=debt_profile_data['bar_width'],
                                   name='Debt Profile', marker_color='deepskyblue', hovertemplate=''))

debt_profile_vuln.add_trace(go.Scatter(x=[debt_profile_data.iloc[2]['x']-2,debt_profile_data.iloc[2]['x']-1,debt_profile_data.iloc[2]['x']], y=[max_point+40]*3, mode='lines',
        name='Upper early warning',
        line=dict(color='mediumslateblue', dash='dash', width=2),
        connectgaps=True, hovertemplate=''
    ))

debt_profile_vuln.add_annotation(x=debt_profile_data.iloc[3]['x']-2, y=max_point+40,
            text="Upper Early Warning",showarrow=False)
    
debt_profile_vuln.add_trace(go.Scatter(x=[debt_profile_data.iloc[0]['x']-2,debt_profile_data.iloc[0]['x']-1,debt_profile_data.iloc[0]['x']], y=[max_point+40,]*3, mode='lines',
        name='Lower early warning',
        line=dict(color='black', dash='dash', width=2),
        connectgaps=True, hovertemplate=''
    ))

debt_profile_vuln.add_annotation(x=debt_profile_data.iloc[1]['x']-2, y=max_point+40,
            text="Lower Early Warning",showarrow=False)

debt_profile_vuln.add_trace(go.Scatter(x=[debt_profile_data.iloc[3]['x'],debt_profile_data.iloc[3]['x']+1], y=[max_point+40,]*2, mode='lines',
        name='Indonesia',
        line=dict(color='deepskyblue', width=4),
        connectgaps=True, hovertemplate=''
    ))

debt_profile_vuln.add_annotation(x=debt_profile_data.iloc[3]['x']+2, y=max_point+40,
            text="Indonesia",showarrow=False)

#add bar name below
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[0]['x'], y=-0.02,
                              xanchor='center', yanchor='top',
                              text=debt_profile_data.iloc[0]['Name'],
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[0]['x'], y=-0.07,
                              xanchor='center', yanchor='top',
                              text='(in basis points)',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[1]['x'], y=-0.02,
                              xanchor='center', yanchor='top',
                              text='External Financing',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[1]['x'], y=-0.07,
                              xanchor='center', yanchor='top',
                              text='Requirement',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[1]['x'], y=-0.12,
                              xanchor='center', yanchor='top',
                              text='(in % of GDP)',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[2]['x'], y=-0.02,
                              xanchor='center', yanchor='top',
                              text="Annual Change",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[2]['x'], y=-0.07,
                              xanchor='center', yanchor='top',
                              text="in Short-Term",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[2]['x'], y=-0.12,
                              xanchor='center', yanchor='top',
                              text="Public Debt",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[2]['x'], y=-0.17,
                              xanchor='center', yanchor='top',
                              text="(in % of GDP)",
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[3]['x'], y=-0.02,
                              xanchor='center', yanchor='top',
                              text='Public Debt Held',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[3]['x'], y=-0.07,
                              xanchor='center', yanchor='top',
                              text='by Non-Residents',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[3]['x'], y=-0.12,
                              xanchor='center', yanchor='top',
                              text='(in % of GDP)',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[4]['x'], y=-0.02,
                              xanchor='center', yanchor='top',
                              text='Public Debt',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[4]['x'], y=-0.07,
                              xanchor='center', yanchor='top',
                              text='in Foreign Currency',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)
debt_profile_vuln.add_annotation(yref='paper', x=debt_profile_data.iloc[4]['x'], y=-0.12,
                              xanchor='center', yanchor='top',
                              text='(in % of GDP)',
                              font=dict(family='Arial',
                                        size=14,
                                        color='#000'),
                              showarrow=False)

debt_profile_vuln.add_hline(y=0.0)

debt_profile_vuln.update_layout(
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
#    autosize=False,
    margin=dict(
#        autoexpand=False,
        l=0,
        r=0,
        t=0,
    ),
    showlegend=False,
    plot_bgcolor='white',
    hovermode=False
)

RISK_HEATMAP = dbc.Card([
    dbc.CardHeader(html.Center(html.H5("Heat Map"))),
    dbc.CardBody([dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=heatmap_risk),md=12)
           ] 
        ),
        html.P(""),
        dbc.Row(
        [
            dbc.Col([
                dbc.CardHeader(html.Center(html.H5("Debt Level Risks"))),
                dbc.CardBody([
                    html.P("Merupakan sensitifitas tingkat utang eksisting terhadap adanya shock pada indikator makroekonomi yang meliputi pertumbuhan GDP, keseimbangan primer, tingkat suku bunga riil, nilai tukar mata uang, dan kewajiban kontinjensi."),
                    html.P(""),
                    html.P("Risiko dipandang rendah jika benchmark beban utang, yaitu 70% dari GDP, tidak akan terlampaui dalam kondisi shock tertentu yang menjadi baseline. Risiko sedang jika benchmark beban utang terlampaui dalam kondisi shock tertentu, namun bukan kondisi yang menjadi baseline. Risiko tinggi, jika benchmark beban utang terlampaui dalam kondisi baseline. Heatmap juga dapat diwarnai putih jika tidak relevan.")
                    ])
                ],md=4),
            dbc.Col([
                dbc.CardHeader(html.Center(html.H5("Gross Financing Needs"))),
                dbc.CardBody([
                    html.P("Merupakan sensitifitas kebutuhan pembiayaan bruto terhadap adanya shock pada indikator makroekonomi yang meliputi pertumbuhan GDP, keseimbangan primer, tingkat suku bunga riil, nilai tukar mata uang, dan kewajiban kontinjensi."),
                    html.P(""),
                    html.P("Risiko dipandang rendah jika benchmark kebutuhan pembiayaan bruto, yaitu 15% dari GDP, tidak akan terlampaui dalam kondisi shock tertentu yang menjadi baseline. Risiko sedang jika benchmark kebutuhan pembiayaan bruto terlampaui dalam kondisi shock tertentu, namun bukan kondisi yang menjadi baseline. Risiko tinggi, jika benchmark kebutuhan pembiayaan bruto terlampaui dalam kondisi baseline. Heatmap juga dapat diwarnai putih jika tidak relevan.")
                    ])
                ],md=4),
            dbc.Col([
                dbc.CardHeader(html.Center(html.H5("Debt Profile"))),
                dbc.CardBody([
                    html.P("Merupakan risiko kesinambungan utang jika ditimbang berdasarkan profil utangnya."),
                    html.P(""),
                    html.P("Terdapat 5 risiko terkait profil utang, yakni bond spreads, kebutuhan pendanaan eksternal, porsi utang publik dalam mata uang asing, perubahan porsi utang jangka pendek, serta porsi utang publik yang dipegang oleh non residen. Kriteria masing-masing risiko dapat dilihat pada bagian Debt Profile Vulnerabilities.")
                    ])
                ],md=4),
            ]
        ),
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
])

DEBT_PROFILE_VULNERABILITIES = dbc.Card([
    dbc.CardHeader(html.Center(html.H5("Debt Profile Vulnerabilities"))),
    dbc.CardBody([dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=debt_profile_vuln),md=12)
            ]
        ),
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
])

HEATMAP = dbc.Container(
    [
     dbc.Row(dbc.Col(RISK_HEATMAP,md=12), style={"marginTop": 50,"marginBottom": 50}),
     dbc.Row(
         [
             dbc.Col(md=6),
             dbc.Col(md=6)
          ], style={"marginTop": 50,"marginBottom": 50}),
     dbc.Row(dbc.Col(DEBT_PROFILE_VULNERABILITIES,md=12), style={"marginTop": 50,"marginBottom": 50})
    ],
    className="mt-12",
)