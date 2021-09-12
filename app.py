import dash
import pathlib
import dash_bootstrap_components as dbc

PATH = pathlib.Path(__file__).parent
ASSETS_PATH = PATH.joinpath("assets").resolve()
STYLES_PATH = ASSETS_PATH.joinpath("styles").resolve()

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
#external_stylesheets = [STYLES_PATH.joinpath('s1.css'),STYLES_PATH.joinpath('styles.css'),BS]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)
server = app.server