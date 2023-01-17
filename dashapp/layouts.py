"""Layouts definitions for Dash app."""
from dash import html, dcc
import dash_bootstrap_components as dbc

load_indicator = dbc.Spinner(html.Div(id='loading'),
                             spinner_style={'width': '3rem', 'height': '3rem'},
                             fullscreen=False,
                             color='danger')
load_info = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle('Detection')),
    dbc.ModalBody(dbc.Alert('', id='load-info-text', color='danger'))],
    id='load-info',
    scrollable=False,
    centered=True,
    is_open=False)

upload = dcc.Upload(["D'n'D or select JPEG"],
                    style={
                        'width'       : '90%',
                        'height'      : '150px',
                        'lineHeight'  : '140px',
                        'borderWidth' : '2px',
                        'borderStyle' : 'dashed',
                        'borderRadius': '10px',
                        'textAlign'   : 'center'},
                    id='upload-data',
                    multiple=False,
                    className='m-3')

image = html.Div([html.Img(src=None, id='image', style={'width': '60vw'})],
                 style={'textAlign': 'center'},
                 className='mt-3')

main_layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div([upload, load_info, load_indicator], className="d-grid gap-2"), width=2),
        dbc.Col([image], width=10)])])

nav_bar = dbc.NavbarSimple(
    brand='Object detection JPEG',
    color='primary',
    dark=True)

app_layout = html.Div([nav_bar,
                       main_layout])
