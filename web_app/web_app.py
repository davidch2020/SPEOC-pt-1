# import packages
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px

# create web app, import bootstrap stylesheet + external stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'])

# Title
title = html.H1(children='My Dash App', style={'textAlign': 'left'}, className='title')

# Navigation bar to get to different pages of the web app
nav_bar = dbc.Nav(className='nav-bar', children=[
    dbc.NavLink(children='Home', href='/home', className='nav-link'),
    dbc.NavLink(children='About', href='/about', className='nav-link'),
    dbc.NavLink(children='Contact', href='/contact', className='nav-link')
], style={'margin': 'auto'})

# Project description tab
project_desc = html.Div(className='box', children=[
    html.H2(children='Project Description', className='box-title', style={'marginBottom': '20px'}),
    # buttons that navigate you through different descriptions of the project
    html.Div(className='slider-container', children=[
        html.Button('\u25C0', id='left_arrow', className='slider-button',
                    style={'float': 'left', 'marginRight': '10px'}),
        html.Span(id='project_desc_text', style={'fontWeight': 'bold', 'textAlign': 'center'}),
        html.Button('\u25B6', id='right_arrow', className='slider-button',
                    style={'float': 'right', 'marginLeft': '10px'})
    ]),
])

# Left tab with map and table options
# Use this to select whether you want a map or table
# Also use this to select what type of map/table you want to show (not implemented yet)
left_tab = html.Div(className='box', children=[
    html.H3(children='Left Tab', className='box-title', style={'textAlign': 'center'}),
    html.Div(className='left-tab-options-container options-container', children=[
        dcc.RadioItems(
            id='left-tab-options',
            options=[
                {'label': 'Map', 'value': 'map'},
                {'label': 'Table', 'value': 'table'}
            ],
            value='map',
            labelStyle={'display': 'block'}
        )
    ]),
], style={'width': '40%', 'height': '600px'})

# Right tab with DataFrame/Map
right_tab = html.Div(className='box', children=[
    html.H3(children='Display', className='box-title', style={'textAlign': 'center'}),
    html.Div(id='right-tab-content',
             style={'overflow': 'scroll'}
             )
], style={'width': '60%', 'height': '600px'})


# call back function that changes the text shown when we move through arrows.
@app.callback(
    Output('project_desc_text', 'children'),
    [Input('left_arrow', 'n_clicks'), Input('right_arrow', 'n_clicks')]
)
def update_project_desc(left_clicks, right_clicks):
    if left_clicks == None:
        left_clicks = 0
    if right_clicks == None:
        right_clicks = 0

    number = 0
    number += right_clicks - left_clicks
    number = number % 10
    return 'This is some text. We are currently displaying text at for the {} slide.'.format(
        number)

# call back function that outputs either map or table depending on your choice
@app.callback(
    Output('right-tab-content', 'children'),
    [Input('left-tab-options', 'value')]
)
def render_right_tab_content(option):
    if option == 'map':
        # placeholder map
        df = px.data.election()  # replace with your own data source
        geojson = px.data.election_geojson()
        fig = px.choropleth(
            df, geojson=geojson, color="Bergeron",
            locations="district", featureidkey="properties.district",
            projection="mercator", range_color=[0, 6500])
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return dcc.Graph(figure = fig)
    elif option == 'table':
        # Display the DataFrame as a table
        df = pd.read_csv('../data_clean/final_data_CD.csv', index_col=0)
        return dash_table.DataTable(
            id='data-table',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            sort_action='native',  # Enable sorting
            filter_action='native',  # Enable filtering
            page_action='native',  # Enable pagination
            page_size=13,  # Number of rows per page
            style_table={'overflowX': 'scroll'},
            style_cell={'minWidth': '150px', 'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        )


# Layout of the app
app.layout = html.Div(className='app-container', children=[
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
    project_desc,
    html.Div(className='tabs-container', children=[left_tab, right_tab])
])

# run app
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
