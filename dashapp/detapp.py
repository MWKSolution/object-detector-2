"""Object detection web app using Dash framework"""
from dash_extensions.enrich import MultiplexerTransform, DashProxy
from dash_bootstrap_components.themes import DARKLY

# from object_detector import Detector
from layouts import app_layout
from callbacks import get_callbacks

# Dash app configuration
app = DashProxy(__name__,
                title='Objects detector',
                external_stylesheets=[DARKLY],
                prevent_initial_callbacks=True,
                transforms=[MultiplexerTransform()])
app.layout = app_layout

# for gunicorn
server = app.server

# detector API end point
DET_API_URL = r'http://detapi:8066/image'

# Dash app callbacks import
get_callbacks(app=app, end_point=DET_API_URL)

if __name__ == '__main__':
    # start web app locally
    app.run_server(port=8050, debug=True)
