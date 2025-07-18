import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# import web app
from app import app

# import info from other pages
from about_us import about_us_layout
from history import history_layout
from data_page import data_layout
from future import future_layout

from maps import maps_layout
from tables import tables_layout

########################################################################################################################
######################################### Define App Components ########################################################
########################################################################################################################
# Title Bar
title = html.H1(children='The Price of Liberty: Hamilton\'s Resolution of the National Debt', style={'textAlign': 'left'}, className='title')

# Navigation bar to get to different pages of the web app
nav_bar = dbc.Nav(className='nav-bar', children=[
    dbc.NavItem(dbc.NavLink("Maps", href="/", className="nav-link", 
                            style={'fontWeight': 'bold'})),
    dbc.NavItem(dbc.NavLink("Tables", href="/tables", className="nav-link", 
                            style={'fontWeight': 'bold'})),
    dbc.DropdownMenu(label = 'Project Details', children = [    
        dbc.NavItem(dbc.NavLink("Historical Background", href="/project_description", 
                                className="nav-link2", style={'fontWeight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Data Description", href="/data_doc", 
                                className="nav-link2", style={'fontWeight': 'bold'})),
        dbc.NavItem(dbc.NavLink("Future Steps", href="/future",
                                className="nav-link2", style={'fontWeight': 'bold'})),
    ],  nav = True, style={'fontWeight': 'bold'}),
    dbc.NavItem(dbc.NavLink("Team", href="/about_us", className="nav-link", style={'fontWeight': 'bold'})),
], style={'margin': 'auto'}, navbar=True)

# Layout of the app
app.layout = html.Div(className='app-container', children=[
    dcc.Location(id='url', refresh=False),
    dbc.Container(className='header-container', children=[
        dbc.Row([
            dbc.Col(title, md=6),
            dbc.Col(
                nav_bar,
                md=6,
                align='end'
            )
        ])
    ]),
    html.Div( id = 'page-content')
])

# Callback to update the page content based on the URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about_us':
        return html.Div([about_us_layout()])
    elif pathname == '/tables':
        return html.Div(tables_layout)
    elif pathname == '/project_description':
        return html.Div([history_layout])
    elif pathname == '/data_doc':
        return html.Div([data_layout])
    elif pathname == '/future':
        return html.Div([future_layout])
    else:
        return html.Div(maps_layout)

server = app.server
# run app
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
