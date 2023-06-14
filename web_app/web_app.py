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

# declare map_df
map_df = gpd.read_file("../data_raw/shapefiles/historicalcounties")

# rename columns and simplify map geometry (to make it run faster)
map_df.rename(columns = {'NHGISNAM':'county'}, inplace = True)
map_df.rename(columns = {'STATENAM':'state'}, inplace = True)
map_df["geometry"] = map_df["geometry"].simplify(0.01).buffer(0)
map_df["Geo_FIPS"] = map_df["Geo_FIPS"].map(lambda x: int(str(x.lstrip("0"))))

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
map_ops = dcc.Checklist(id="st_checklist", options=[" Total State Population", " Total Slave Population", 
                                 " Total Number of Debt Holders", " Percentage Debt Holders Nationally", 
                                 " Total Amount of Debt", " Percentage of Total National Debt", " Occupations with Most Debt"], 
                        value=[" Display Total State Population"])

# title: "map options"
map_op_title = html.H5(children="State Options", id="map_op_title")

# dropdown menu of states 
state_pops = pd.read_csv("../data_raw/census_data/statepop.csv")
states = state_pops["State"].dropna()
states = pd.concat([pd.Series(["All States"]), states]).tolist()

# remove states that have no map data 
states.remove("Maine")
states.remove("Kentucky")
states.remove("Tennessee")

states_drp = dcc.Dropdown(
    id="states_drpdwn",
    options=states,
    value=states[0]
)

# title : "Pick a state"
st_title = html.H5(children="Choose a State")

# title : "state information"
st_info_title = html.H5(children="State Info")

# Left tab with map and table options
# Use this to select whether you want a map or table
# Also use this to select what type of map/table you want to show (not implemented yet)
left_tab = html.Div(id="left_tab", className='box', children=[
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
        st_title,
        states_drp 
    ], style={"display":"block"}), 
    html.Div(id="state_ops", children=[
        map_op_title,
        map_ops
    ], style={"display":"block"}), 
    html.Div(id="c_drpdwn",
              style={"display":"block"}),
    html.Div(id="st_info", children=[
        st_info_title,
        html.Ul(id="st_infolist")
    ])
], style={'width': '40%', 'height': 'auto', "display":"block"})

# Right tab with DataFrame/Map
right_tab = html.Div(className='box', children=[
    html.H3(children='Display', className='box-title', style={'textAlign': 'center'}),
    html.Div(id='right-tab-content', 
                style={'overflow': 'scroll'}
             )
], style={'width': '60%', 'height': '600px'})

# get checked box values /x/
# find data for each checked box 
# populate div with id=st_info 
    # store data in a <ul> element : with individual <li> 
@app.callback(
        Output("st_infolist", "children"), 
        [Input("st_checklist", "value"),
        Input("states_drpdwn", "value")]
)
def handle_state_ops(options, sel_state):
    display_items = []

    # remove whitespace at the beginning
    for i in range(len(options)):
        options[i] = options[i].strip()
    
    for option in options:
        if option == "Total State Population":
            tot_st_pop = state_pops.loc[state_pops["State"] == sel_state, "Total Pop"].iloc[0]
            display_items.append(html.Li(html.B(children="Total State Population")))
            display_items.append(tot_st_pop)
        elif option == "Total Slave Population":
            tot_sl_pop = state_pops.loc[state_pops["State"] == sel_state, "Slave Pop"].iloc[0]
            display_items.append(html.Li(html.B(children="Total Slave Population")))
            display_items.append(tot_sl_pop) 
        elif option == "Total Number of Debt Holders":
            tot_sl_pop = state_pops.loc[state_pops["State"] == sel_state, "Slave Pop"].iloc[0]
            display_items.append(html.Li(html.B(children="Total Slave Population")))
            display_items.append(tot_sl_pop) 

    return display_items
# call back function to display dropdown menus when 'map' is clicked
@app.callback( 
        [Output("st_c_drpdwn", "style"),
         Output("c_drpdwn", "style")],
        Input("left-tab-options", "value")
)
def add_map_options(value):
    if value == "map":
        return {"display":"block"}, {"display":"block"}
    else:
        return {"display":"none"}, {"display":"none"}

# call back function to display map options when 'map' is clicked 
@app.callback( 
        Output("state_ops", "style"),
        [Input("left-tab-options", "value"), 
         Input("states_drpdwn", "value")]
)
def add_map_options(value, state):
    if value == "map" and state != "All States":
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

# when state is chosen, display county dropdown 
@app.callback(
    Output("c_drpdwn", "children"),
    Input("states_drpdwn", "value")
)
def display_c_drpdwn(value):
    if value != "All States":
        counties = map_df.query("state==" + "'" + value + "'")["county"].tolist()
        counties.insert(0, "Not Selected")
        # title: "choose a county"
        c_drpdwn_title = html.H5(children="Choose a County", id="c_drpdwn_t")
        c_drp = dcc.Dropdown(
            id="county_drpdwn",
            options=counties,
            value=counties[0]
        )
        return c_drpdwn_title, c_drp 
    else:
        return ''

@app.callback(
        Output('right-tab-content', 'children'),
        [Input("states_drpdwn", "value"),
        Input("left-tab-options", "value")] 
)
def handle_state_dropdown(state, option):
    if option == "map":
        fitbounds = False
        basemap_visible = True
        map_df_c = map_df.copy()

        if (state != "All States"):
            map_df_c = map_df_c.loc[map_df['state'] == state]
            fitbounds = "locations"
            basemap_visible = False

        # save as a geojson
        map_str = map_df_c.to_json()
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
                                hover_name="County",
                                hover_data="Population"
                            )

        return dcc.Graph(figure = fig)
    else: # option is table
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
