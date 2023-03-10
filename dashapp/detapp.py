"""Object detection web app using Dash framework"""
from dash import Dash
from dash_bootstrap_components.themes import DARKLY
from dash.long_callback import CeleryLongCallbackManager
from celery import Celery

from layouts import app_layout
from callbacks import get_callbacks_as_tasks

# detector API end point
DET_API_URL = r'http://detapi:8066/image'

# celery tasks queue
celery_app = Celery('worker',
                    broker="redis://redis:6379/0",
                    backend="redis://redis:6379/1")

# setting up dash app: callback_manager, dash app, layouts, callbacks
long_callback_manager = CeleryLongCallbackManager(celery_app)
dash_app = Dash('detector',
                title='Objects detector',
                external_stylesheets=[DARKLY],
                long_callback_manager=long_callback_manager,
                prevent_initial_callbacks=True)
dash_app.layout = app_layout
get_callbacks_as_tasks(app=dash_app, end_point=DET_API_URL)

# for gunicorn
server = dash_app.server


if __name__ == '__main__':
    # start web app locally
    dash_app.run_server(port=8050, debug=True)
