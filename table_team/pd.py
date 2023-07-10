import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Project Description'),

    html.Div(children='''
        [Insert Project Description Here].
    '''),

])
