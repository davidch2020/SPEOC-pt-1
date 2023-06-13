# import packages
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px
import geopandas as gpd
import topojson as tp
import json
import dash_leaflet as dl

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

# map options
map_ops = dcc.Checklist(options=[" Display Total Population", " Display Total Slave Population", 
                                 " Display Towns", " Total Debt Ownership", " Percentage Debt Ownership",
                                  " Occupations With Highest Debt Ownership" ], 
                        value=[" Display Total Population"])

# title: "map options"
map_op_title = html.H5(children="Map Options", id="map_op_title")

# dropdown menu of states 
state_pops = pd.read_csv("../data_raw/census_data/statepop.csv")
states = state_pops["State"].dropna()
states = pd.concat([pd.Series(["All States"]), states])
states_drp = dcc.Dropdown(
    id="states_drpdwn",
    options=states,
    value=states[0]
)

# title: "choose a state and a county"
drpdwn_title = html.H5(children="Choose a State and a County", id="drpdwn_title")

"""
Hold off on this for now 
# dropdown menu of counties 
# find all the state codes
# use a for loop to go through each state code and 
county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv")
state_codes = county_pops["State/US Abbreviation"].dropna().unique().tolist()
del state_codes[0]
print(state_codes)
"""

# import map shapefile
map_df = gpd.read_file("../data_raw/shapefiles/historicalcounties")

map_df.rename(columns = {'NHGISNAM':'county'}, inplace = True)
map_df.rename(columns = {'STATENAM':'state'}, inplace = True)

map_gj = map_df.to_json()
print(type(map_df))

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
    html.Div(id="st_c_drpdwn", children=[
        drpdwn_title,
        states_drp 
    ], style={"display":"block"}), 
    html.Div(id="map_ops", children=[
        map_op_title,
        map_ops
    ], style={"display":"block"}) 
], style={'width': '40%', 'height': '600px'})

# Right tab with DataFrame/Map
right_tab = html.Div(className='box', children=[
    html.H3(children='Display', className='box-title', style={'textAlign': 'center'}),
    html.Div(id='right-tab-content', 
                style={'overflow': 'scroll'}
             )
], style={'width': '60%', 'height': '600px'})

# call back function to display dropdown menus when 'map' is clicked
@app.callback( 
        Output("st_c_drpdwn", "style"),
        Input("left-tab-options", "value")
)
def add_map_options(value):
    if value == "map":
        return {"display":"block"}
    else:
        return {"display":"none"}

# call back function to display map options when 'map' is clicked 
@app.callback( 
        Output("map_ops", "style"),
        Input("left-tab-options", "value")
)
def add_map_options(value):
    if value == "map":
        return {"display":"block"}
    else:
        return {"display":"none"}

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

# create national choropleth map 
# import map shapefile
map_df = gpd.read_file("../data_raw/shapefiles/historicalcounties")

# rename columns and simplify map geometry (to make it run faster)
map_df.rename(columns = {'NHGISNAM':'county'}, inplace = True)
map_df.rename(columns = {'STATENAM':'state'}, inplace = True)
map_df["geometry"] = map_df["geometry"].simplify(0.01).buffer(0)

# save as a geojson
map_str = map_df.to_json()
map_gj = json.loads(map_str) # convert string json to dictionary json 

# get county populations 
county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
county_pops = county_pops[county_pops["SE_T001_001"].notna()]
county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
county_pops = county_pops[["Geo_FIPS", "SE_T001_001"]]
county_pops.rename(columns = {'SE_T001_001':'population'}, inplace = True)

@app.callback(
        Output('right-tab-content', 'children'),
        Input("states_drpdwn", "value")
)
def handle_state_dropdown(state):
    print("State=" + state)
    fitbounds = False
    basemap_visible = True
    map_df = gpd.read_file("../data_raw/shapefiles/historicalcounties")

    # rename columns and simplify map geometry (to make it run faster)
    map_df.rename(columns = {'NHGISNAM':'county'}, inplace = True)
    map_df.rename(columns = {'STATENAM':'state'}, inplace = True)
    map_df["geometry"] = map_df["geometry"].simplify(0.01).buffer(0)

    if (state != "All States"):
        map_df = map_df.loc[map_df['state'] == state]
        fitbounds = "locations"
        basemap_visible = False

    # save as a geojson
    map_str = map_df.to_json()
    map_gj = json.loads(map_str) # convert string json to dictionary json 

    # get county populations 
    county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
    county_pops = county_pops[county_pops["SE_T001_001"].notna()]
    county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
    county_pops.rename(columns = {'SE_T001_001':'Population', "Geo_name":"County"}, inplace = True)
    county_pops = county_pops[["Geo_FIPS", "Population", "County"]]

    # create choropleth map 
    fig = px.choropleth(county_pops, geojson=map_gj, locations='Geo_FIPS', color='Population',
                            color_continuous_scale="Viridis",
                            range_color=(county_pops["Population"].min(), county_pops["Population"].max()),
                            featureidkey="properties.Geo_FIPS",
                            scope="usa",
                            basemap_visible=basemap_visible,
                            fitbounds=fitbounds,
                            hover_data=["County"]
                        )

    return dcc.Graph(figure = fig)

# call back function that outputs either map or table depending on your choice

"""
@app.callback(
    Output('right-tab-content', 'children'),
    [Input('left-tab-options', 'value')]
)
def render_right_tab_content(option):
    if option == 'map':
        # create choropleth map 
        fig = px.choropleth(county_pops, geojson=map_gj, locations='Geo_FIPS', color='population',
                                color_continuous_scale="Viridis",
                                range_color=(county_pops["population"].min(), county_pops["population"].max()),
                                featureidkey="properties.Geo_FIPS",
                                scope="usa",
                                basemap_visible=False,
                                fitbounds="locations"
                            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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
"""

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
