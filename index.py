import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from layouts import layout1, layout2, layout3, layout4, layout5
import callbacks

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app.layout = html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Basic DSA", header=True),
                dbc.DropdownMenuItem("Baseline Scenario", href="/"),
                dbc.DropdownMenuItem("Public Debt Composition and Alt. Scenario", href="/public-debt-composition-and-alternative-scenario"),
            ],
            nav=True,
            in_navbar=True,
            label="Basic DSA",
        ),
        dbc.NavItem(dbc.NavLink("Realism of Baseline Assumptions", href="/realism-of-baseline-assumptions")),
        dbc.NavItem(dbc.NavLink("Stress Tests", href="/stress-tests")),
        dbc.NavItem(dbc.NavLink("Risk Assessment", href="risk-assessment"))
    ],
    brand="Debt Sustainability Analytics",
    brand_href="/",
    color="primary",
    dark=True,
),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([#start of footer div
        html.P("© 2021 - Lantai Sebelas Inspektorat Jenderal", style={"font-weight":"bold"})
        ],className="pretty_container", style={'text-align':'center'}
        )#end of footer div
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout1
    elif pathname == '/public-debt-composition-and-alternative-scenario':
        return layout2
    elif pathname == '/realism-of-baseline-assumptions':
        return layout3
    elif pathname == '/stress-tests':
        return layout4
    elif pathname == '/risk-assessment':
        return layout5 
    elif pathname == '/page6':
        return layout6
    elif pathname == '/page7':
        return layout7    
    elif pathname == '/page8':
        return layout8
    elif pathname == '/page9':
        return layout9
    elif pathname == '/page10':
        return layout10
    elif pathname == '/page11':
        return layout11    
    elif pathname == '/page12':
        return layout12
    elif pathname == '/page13':
        return layout13
    elif pathname == '/page14':
        return layout14
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)