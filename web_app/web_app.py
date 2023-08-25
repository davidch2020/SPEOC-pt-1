# import packages
import math
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import plotly.express as px
import geopandas as gpd
import json
import numpy as np

# import json file that converts full name of a state to two character abbreviation
with open('assets/state_codes.json',"r") as file:
    state_codes = json.load(file)

########################################################################################################################
###################################### dataframes used for maps ########################################################
########################################################################################################################
# contains county borders
map_df = gpd.read_file("../data_raw/shapefiles/historicalcounties")
# rename columns and simplify map geometry (to make it run faster)
map_df.rename(columns = {'NHGISNAM':'county'}, inplace = True)
map_df.rename(columns = {'STATENAM':'state'}, inplace = True)
map_df['state_abrev'] = map_df.loc[:, 'state']
map_df.replace({"state_abrev": state_codes}, inplace = True) 
map_df["geometry"] = map_df["geometry"].simplify(0.01).buffer(0)
map_df["Geo_FIPS"] = map_df["Geo_FIPS"].map(lambda x: int(str(x.lstrip("0"))))

# only contains state borders
state_map_df = gpd.read_file("../data_raw/shapefiles/stateshape_1790")
state_map_df.rename(columns = {'STATENAM':'state'}, inplace = True)
state_map_df['state_abrev'] = state_map_df.loc[:, 'state']
state_map_df.replace({"state_abrev": state_codes}, inplace = True)

# list of states we include in dropdown menu
state_pops = pd.read_csv("../data_raw/census_data/statepop.csv")
states = state_pops["State"].dropna()
states = pd.concat([pd.Series(["All States"]), states]).tolist()
# remove states that have no map data
states.remove("Maine")
states.remove("Kentucky")
states.remove("Tennessee")

########################################################################################################################
######################################### define app components ########################################################
########################################################################################################################
# create web app, import bootstrap stylesheet + external stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'], \
                suppress_callback_exceptions = True)

# Title Bar
title = html.H1(children='American National Debt in the 18th Century', style={'textAlign': 'left'}, className='title')

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


# Information Content for Region Filter
region_title = html.H5(children=["Region", html.Button(children='ℹ', className='more_info_btn', id='more_info_regions', n_clicks=0)])
regions_drop = dcc.Dropdown(
    id = "reg_drpdwn",
    options=['Not Selected','Nation','State','County'],
    value = 'Not Selected'
)

rangeslider = dcc.RangeSlider(id="slider", min = 0, max = 10)
rangeslider2 = dcc.RangeSlider(id="slider-2", min = 0, max = 10)

# Left tab with map and table options
# Use this to select whether you want a map or table
# Also use this to select what type of map/table you want to show (not implemented yet)

left_tab = html.Div(id="left_tab", className='box', children=[
    html.H3(children='Customize', className='box-title', style={'textAlign': 'center'}),

    html.Div(id="regions_c_drpdwn", children=[
        region_title,
        regions_drop, 
        dbc.Modal(
            [
                dbc.ModalHeader("Parameter Description: Region"),
                dbc.ModalBody("Region determines the geographical scope of the displayed map. Nation shows the entire US, " + \
                    "State shows a given state (that you pick) and County shows a county in a state (that you pick).")
            ], 
            id='regions_modal' 
        ), 
        dbc.Modal(
            [
                dbc.ModalHeader("Parameter Description: Border"),
                dbc.ModalBody("Border determines the level of geographical aggregation. " + \
                              "For example, you can examine a nation-wide map at the county, state or national level")

            ],
            id='border_type_modal' 
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Parameter Description: Statistic"),
                dbc.ModalBody("Statistic determines what metric the map displays. For example, Population shows you, at each unit" + \
                              " of your border, the population.")
            ],
            id='heatmap_modal'
        )

    ], style={"display":"block"}), 
    html.Div(id="states_c_drpdwn", children=[
        dcc.Dropdown(id="states_drpdwn", style={"display":"none"})
    ]), 
    html.Div(id="c_drpdwn", children=[
        dcc.Dropdown(id="county_drpdwn", style={"display":"none"})
    ]), 
    html.Div(id="bord_c_drpdwn", children=[
        dcc.Dropdown(id="border_drpdwn", style={"display":"none"}),
    ]), 
    html.Div(id="heatmap_c_drpdwn", children=[
        dcc.Dropdown(id="heatmap_drpdwn", style={"display":"none"}),
    ]),
    # dcc.Checklist(
    #     options=['Compare Two Heatmaps'],
    #     id='compare_checkbox',
    #     style={'display':'block'}
    # ),
    # html.Div(id='heatmap_c_drpdwn_2', children=[
    #     dcc.Dropdown(id='heatmap_drpdwn_2', style={'display':'none'})
    # ])
], style={'width': '50%', 'height': 'auto', "display":"block"})

right_tab = html.Div(id="right_tab", className='box', children=[
    html.H3(children='Statistics', className='box-title', style={'textAlign': 'center'}),
], style={'width': '50%', 'height': 'auto', "display":"block"})

# Bottom Display tab with DataFrame/Map
display_tab = html.Div(className='box', children=[
    html.H3(children='Display', className='box-title', style={'textAlign': 'center'}),
    html.Div(id='right-tab-content', 
                style={'overflow': 'scroll'}
             ),
    html.Div(id = "range-slider", children=[ 
        rangeslider
    ], style={"display":"none"})
], style={'width': '100%', 'height': '600px'})

# Right tab 2 with the map you want to compare with
# right_tab_2 = html.Div(className='box', children=[
#     html.H3(children='Display', className='box-title', style={'textAlign':'center'}),
#     html.Div(id='right-tab-content-2',
#              style={'overflow':'scroll'}
#              ),
#     html.Div(id = "range-slider-2", children=[
#         rangeslider2
#     ], style={"display":"none"})
# ], style={'width': '100%', 'height': '600px'})


# Callback functions to handle additional information button 
@app.callback(
        Output('regions_modal', 'is_open'),
        Input('more_info_regions', 'n_clicks')
)
def open_regions_information(n_clicks):
    if n_clicks > 0:
        return True     
    else:
        return False


# call back function to display range slider when heatmap type is chosen
@app.callback( 
        Output("range-slider", "style"),
        [Input("heatmap_drpdwn", "value")]
)
def add_range_slider(heatvalue):
    if (heatvalue is not None) and (heatvalue != "Not Selected"):
        return {"display":"block"}
    else:
        return {"display":"none"}

# call back function to display second range slider when heatmap type is chosen
@app.callback( 
        Output("range-slider-2", "style"),
        [Input("heatmap_drpdwn_2", "value")]
)
def add_range_slider_2(heatvalue):
    if (heatvalue is not None) and (heatvalue != "Not Selected"):
        return {"display":"block"}
    else:
        return {"display":"none"}

#when state/county is chosen as the region, display state dropdown
@app.callback(
    Output("states_c_drpdwn", "children"),
    Input("reg_drpdwn", "value")
)
def display_state_drpdwn(value):
    # Different titles if you're picking a state for a county or just a state
    if value == "State":
        state_drpdwn_title = html.H5(children="Pick a State", id="state_drpdwn_t", style = {"margin-left": "200px"})
    elif value == 'County':
        state_drpdwn_title = html.H5(children="State of Your County", id="state_drpdwn_t", style = {"margin-left": "200px"})
    else:
        return ''
    state_drp = dcc.Dropdown(
        id="states_drpdwn",
        options=states,
        value=states[0],
        style = {'width': '70%', "margin-left": "100px"}
    )
    return state_drpdwn_title, state_drp


#when state of the county is chosen, display county dropdown
@app.callback(
    Output("c_drpdwn", "children"),
    [Input("states_drpdwn", "value"),
    Input("reg_drpdwn","value")]
)
def display_county_drpdwn(state_value, reg_value):
    if reg_value != "County":
        return ''
    if (state_value != "All States") and (state_value is not None):
        counties = map_df.query("state==" + "'" + state_value + "'")["county"].tolist()
        counties.insert(0, "All Counties")
        county_drpdwn_title = html.H5(children="Choose a County", id="county_drpdwn_t", style = {"margin-left": "200px"})
        county_drp = dcc.Dropdown(
            id="county_drpdwn",
            options=counties,
            value=counties[0],
            style = {'width': '70%', "margin-left": "100px"} 
        )
        return county_drpdwn_title, county_drp 
    else:
        return ''

# when region is chosen, display border dropdown 
@app.callback(
    Output("bord_c_drpdwn", "children"),
    [Input("reg_drpdwn", "value"),
     Input("states_drpdwn", "value"),
     Input("county_drpdwn", "value")]
)
def display_border_drpdwn(reg_value, state_value, county_value): 
    if (reg_value != "Not Selected") and (reg_value is not None):
        if (reg_value == "State") and (state_value == "All States") or (reg_value == "County") and (state_value=="All States") \
            or (reg_value == "County") and (county_value == "All Counties"):
            return ''
        bord_drpdwn_title = html.H5(children=["Border", html.Button(children="ℹ", className='more_info_btn', id="more_info_border_button")], id="bord_drpdwn_t")
        if reg_value == "Nation":
            drpdown_options = ['Not Selected', 'Nationwide', 'Statewide', 'Countywide']
        elif reg_value == "State":
            drpdown_options = ['Not Selected', 'Statewide', 'Countywide']
        elif reg_value == "County":
            drpdown_options = ['Not Selected', 'Countywide']

        bord_drp = dcc.Dropdown(
            id="border_drpdwn",
            options=drpdown_options,
            value='Not Selected'
        )
        return bord_drpdwn_title, bord_drp 
    else:
        return ''

# Display more information about what border type means 
@app.callback(
        Output("border_type_modal", "is_open"),
        Input('more_info_border_button', 'n_clicks'),
        State('border_type_modal', 'is_open')
)
def open_border_type_modal(n_click, state):
    if n_click:
        return not state 
    return state 

#when border is chosen, display heatmap dropdown
@app.callback(
    Output("heatmap_c_drpdwn", "children"),
    [Input("border_drpdwn", "value"), #need more input so it doesnt show up in county/state ex
    Input("reg_drpdwn", "value")]
)
def display_heatmap_drpdwn(border_value, region_value):
    if (border_value != "Not Selected") and (border_value is not None):
        heatmap_chklist_title = html.H5(children=["Statistic", html.Button(children='ℹ', className='more_info_btn', id='heatmap_more_info_button')], id="heatmap_drpdwn_t")
        heatmap_drp = dcc.Dropdown(
            id="heatmap_drpdwn",
            options=['Not Selected', 'Population', 'Slave Population', 'Debt Density', 'Debt Distribution', 'Average Debt Holdings'],
            value="Not Selected"
        )
        return heatmap_chklist_title, heatmap_drp
    else:
        return ''

# Set 'compare two heatmaps' visiblity checkbox to True
# @app.callback(
#     Output("compare_checkbox", "style"),
#     [Input("border_drpdwn", "value"), #need more input so it doesnt show up in county/state ex
#     Input("reg_drpdwn", "value"),
#     Input("heatmap_drpdwn", "value")]
# )
# def display_checkbox(border_value, option, heatmap):
#     if (border_value == "Not Selected") or (border_value is None) or (option != "map") or (heatmap == "Not Selected") or (heatmap is None):
#         return {'display':'none'}
#     else:
#         return {'display':'block'}
#
# If the `compare two heatmaps` checkbox was clicked, create a new heatmap dropdown. 
# @app.callback(
#     Output('heatmap_c_drpdwn_2', 'children'),
#     [Input('compare_checkbox', 'value')]
# )
# def create_new_heatmap(values):
#     if values is None:
#         return ''
#     value = values[0]
#     if value == 'Compare Two Heatmaps':
#         heatmap_title = html.H5(children=["Pick a Heatmap to Compare With"], id="heatmap_drpdwn_t")
#         heatmap_drp = dcc.Dropdown(
#             id="heatmap_drpdwn_2",
#             options=['Not Selected', 'Population', 'Slave Population', 'Debt Density', 'Debt Distribution', 'Average Debt Holdings'], #add more if more needed
#             value= "Not Selected"
#         )
#         return heatmap_title, heatmap_drp
#     else:
#         return ''

@app.callback(
    Output("heatmap_modal", "is_open"),
    Input('heatmap_more_info_button', 'n_clicks'), 
    State('heatmap_modal', 'is_open')
)
def open_heatmap_more_info(n_clicks, state):
    if n_clicks:
        return not state 
    return state

@app.callback(
        Output('right-tab-content', 'children'),
        Output('range-slider', 'children'),
        [Input("states_drpdwn", "value"), 
        Input("county_drpdwn", "value"),
        Input('heatmap_drpdwn', 'value'),
        Input('border_drpdwn', 'value'),
        Input('slider', 'value'),
        Input('slider', 'max')] #to keep track of when the heatmap type changes--> means that the rangeslider maximum must be adjusted 
)

def handle_state_dropdown(state, county, map_type, border_type, sliderrange, slidermax):
    global fig

    fitbounds = False
    basemap_visible = True
    map_df_c = map_df.copy()
    state_map_df_c = state_map_df.copy()

    # save as a geojson
    map_str = map_df_c.to_json()
    map_gj = json.loads(map_str) # convert string json to dictionary json

    states_str = state_map_df_c.to_json()
    states_gj = json.loads(states_str)

    if (map_type == "Not Selected") or (map_type is None):
        return '', rangeslider

    if (state != "All States") and (state is not None):
        if border_type == "Countywide":
            map_df_c = map_df_c.loc[map_df['state'] == state]
        if border_type == "Statewide" or border_type == "Nationwide":
            state_map_df_c = state_map_df_c.loc[state_map_df['state']==state]
        fitbounds = "locations"
        basemap_visible = False

    if (county != "All Counties") and (county is not None):
        map_df_c = map_df_c.loc[map_df_c['county'] == county]

    # save as a geojson
    map_str = map_df_c.to_json()
    map_gj = json.loads(map_str) # convert string json to dictionary json

    states_str = state_map_df_c.to_json()
    states_gj = json.loads(states_str)


    # debt info per county
    debt_by_county = pd.read_csv("../data_clean/final_data_CD.csv")[["Group State", "Group County", '6p_total']]
    debt_by_county = debt_by_county.groupby(by=["Group County", "Group State"]).agg(['size', 'sum'])
    # debt_by_county = debt_by_county.to_frame()
    # debt_by_county.rename(columns={'size':'count'}, inplace=True)
    debt_by_county.reset_index(inplace=True)

    debt_by_county.columns = debt_by_county.columns.droplevel(1)
    debt_by_county.columns = ['county', 'state', 'count', '6p_total']

    county_geo_fips = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)[["Geo_FIPS", "Geo_name", 'Geo_STUSAB', "SE_T001_001"]]
    county_geo_fips.rename(columns={"Geo_name":"county", 'Geo_STUSAB':'state', "SE_T001_001":'population'}, inplace=True)
    county_debt_geo = pd.merge(debt_by_county, county_geo_fips, on=["county", 'state'])

    state_sixp_agg = county_debt_geo.groupby('state', as_index = False).sum()
    state_sixp_agg.drop('Geo_FIPS', inplace=True, axis = 1) #the summing messes it up; also not necessary for states anyways

    if map_type == 'Population':

        # get county populations
        county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
        county_pops = county_pops[county_pops["SE_T001_001"].notna()]
        county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
        county_pops.rename(columns = {'SE_T001_001':'Population', "Geo_name":"County"}, inplace = True)
        county_pops = county_pops[["Geo_FIPS", "Population", "County"]]

        #state pop
        state_pops = gpd.read_file("../data_raw/census_data/statepop.csv")
        state_pops = state_pops[["State", "Total Pop"]].head(15)
        state_pops = state_pops.astype({"Total Pop":"int"})

        # create choropleth map based on border type
        if border_type == "Countywide":

            county_pops_adj = county_pops.copy()

            if slidermax != county_pops["Population"].max(): #when the map is loaded for the first time, maximum value will not match county_pops["Population"].max()
                slider =  dcc.RangeSlider(min = 0,
                                max = county_pops["Population"].max(),
                                id = "slider"
                                )
            else: #otherwise, this is the case where the map was not loaded for the first time, and the user just adjusted the rangeslider
                slider =  dcc.RangeSlider(min = 0,
                                max = county_pops["Population"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                county_pops_adj = county_pops[county_pops['Population'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(county_pops_adj, geojson=map_gj, locations='Geo_FIPS',
                    color='Population',
                    color_continuous_scale="Viridis",
                    range_color=(county_pops["Population"].min(),
                                county_pops["Population"].max()),
                    featureidkey="properties.Geo_FIPS",
                    scope="usa",
                    basemap_visible=basemap_visible,
                    fitbounds=fitbounds,
                    hover_name="County",
                    hover_data=["Population"],
                )

        elif border_type == "Statewide":

            state_pops_adj = state_pops.copy()

            if slidermax != state_pops["Total Pop"].max():
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pops["Total Pop"].max(),
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pops["Total Pop"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                state_pops_adj = state_pops[state_pops['Total Pop'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(state_pops_adj, geojson=states_gj, locations='State',
                                color='Total Pop',
                                color_continuous_scale="Viridis",
                                range_color=(state_pops["Total Pop"].min(),
                                            state_pops["Total Pop"].max()),
                                featureidkey="properties.state",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="State",
                                hover_data=["Total Pop"]
                        )

        elif border_type == "Nationwide":

            nat_pops = state_pops.copy()

            nat_val = state_pops["Total Pop"].sum()
            national = [nat_val]*15
            nat_pops["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                nat_pops = nat_pops[nat_pops['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_pops, geojson=states_gj, locations='State',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="State",
                                hover_data= ["National"]
                        )


    elif map_type == 'Slave Population':

        #basemap_visible = True
        county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
        county_pops = county_pops[county_pops["SE_T001_001"].notna()]
        county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
        county_pops.rename(columns = {'SE_T001_001':'Population', "Geo_name":"County"}, inplace = True)

        county_slaves = gpd.read_file("../data_raw/census_data/census.csv")
        county_slaves = county_slaves[["GISJOIN", "slavePopulation"]].head(290)
        county_slaves['GISJOIN'] = county_slaves['GISJOIN'].str.replace('G0', '')
        county_slaves['GISJOIN'] = county_slaves['GISJOIN'].str.replace('G', '') #convert to geo_fips
        county_slaves.rename(columns = {'GISJOIN':'Geo_FIPS'}, inplace = True)
        merged = pd.merge(county_pops, county_slaves, on=['Geo_FIPS'])
        merged = merged[["Geo_FIPS", "slavePopulation", "County"]]
        merged = merged.astype({"slavePopulation":"int", "Geo_FIPS":"str"})
        #print(merged)

        state_pop = gpd.read_file("../data_raw/census_data/statepop.csv")
        state_pop = state_pop[["State", "Slave Pop"]].head(15)
        state_pop = state_pop.astype({"Slave Pop":"int"})

        if border_type == "Countywide":
            county_slaves_adj = merged.copy()

            #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            #    print(county_slaves_adj)

            if slidermax != merged["slavePopulation"].max(): #issue with choosing state of max county
                slider =  dcc.RangeSlider(min = 0,
                                max = merged["slavePopulation"].max(),
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = merged["slavePopulation"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                county_slaves_adj = merged[merged['slavePopulation'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(county_slaves_adj, geojson=map_gj, locations='Geo_FIPS',
                    color='slavePopulation',
                    #color_continuous_scale="Viridis",
                    range_color=(merged["slavePopulation"].min(),
                                merged["slavePopulation"].max()),
                    featureidkey="properties.Geo_FIPS",
                    scope="usa",
                    basemap_visible=basemap_visible,
                    fitbounds=fitbounds,
                    hover_name="County",
                    hover_data=["slavePopulation"],
                    color_continuous_scale=[[0, 'rgb(240,240,240)'],
                            [0.1, 'rgb(126, 191, 113)'],
                            [0.2, 'rgb(91, 161, 77)'],
                            [0.75, 'rgb(227, 72, 54)'],
                            [1, 'rgb(227, 26, 28)']]
                )


        elif border_type == "Statewide":
            state_pop_adj = state_pop.copy()

            if slidermax != state_pop["Slave Pop"].max():
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pop["Slave Pop"].max(),
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pop["Slave Pop"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                state_pop_adj = state_pop[state_pop['Slave Pop'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(state_pop_adj, geojson=states_gj, locations='State', #map_gj vs states_gj
                        color='Slave Pop',
                        color_continuous_scale="Viridis",
                        range_color=(state_pop['Slave Pop'].min(),
                                    state_pop['Slave Pop'].max()),
                        featureidkey="properties.state",
                        scope="usa",
                        basemap_visible=basemap_visible,
                        fitbounds=fitbounds,
                        hover_name="State",
                        hover_data=["Slave Pop"]
                    )

        elif border_type == "Nationwide":

            nat_slave = state_pop.copy()

            nat_val = state_pop["Slave Pop"].sum()
            national = [nat_val]*15
            nat_slave["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                nat_slave = nat_slave[nat_slave['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_slave, geojson=states_gj, locations='State',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="State",
                                hover_data= ["National"]
                        )

    elif map_type == 'Debt Distribution':
        # Create the debt distribution map
        # Input: archive/.../CD_geographical_table_summary.csv, countyPops.csv (GEO_FIPS column), Map geojson file
        # Create a dataframe of all county names and their GEO_FIPS code
        # Merge dataframe with CD_geographical_table_summary.csv
        # test debt distribution map
        # fig = px.choropleth()
        six_p_tot = county_debt_geo["6p_total"]


        x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

        #print(six_p_tot[six_p_tot.between(six_p_tot.quantile(.85), six_p_tot.quantile(1))])

        Q1 = np.percentile(county_debt_geo['6p_total'], 25, method='midpoint')
        Q3 = np.percentile(county_debt_geo['6p_total'], 75, method='midpoint')
        IQR = Q3 - Q1

        # Above Upper bound
        upper=Q3+1.5*IQR
        upper_array=np.array(county_debt_geo['6p_total']>=upper)

        #Below Lower bound
        lower=Q1-1.5*IQR
        lower_array=np.array(county_debt_geo['6p_total']<=lower)

        xiv = pd.Interval(x.min(), x.max())
        xmid = xiv.mid
        print(xmid)


        if border_type == "Countywide": #automatic rounding issue. See explanation in debt density section

            ceiling_var = county_debt_geo["6p_total"].max() + 1000 #so that the slider does not round down and exclude the actual max value

            county_debt_geo_adj = county_debt_geo.copy()
            if slidermax != ceiling_var:
                slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                county_debt_geo_adj = county_debt_geo[county_debt_geo['6p_total'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(county_debt_geo_adj, geojson=map_gj, locations='Geo_FIPS',
                        color='6p_total',
                        #color_continuous_scale="Viridis",
                        range_color=(county_debt_geo['6p_total'].min(),
                                    county_debt_geo['6p_total'].max()),
                        featureidkey="properties.Geo_FIPS",
                        scope="usa",
                        basemap_visible=basemap_visible,
                        fitbounds=fitbounds,
                        hover_name="county",

                        hover_data=["6p_total"],
                        color_continuous_scale=[[0, 'rgb(240,240,240)'],
                            [0.1, 'rgb(126, 191, 113)'],
                            [0.2, 'rgb(91, 161, 77)'],
                            [0.75, 'rgb(227, 72, 54)'],
                            [1, 'rgb(227, 26, 28)']]
                    )
        elif border_type == "Statewide":

            ceiling_var = state_sixp_agg["6p_total"].max() + 1000 #same reasoning as for county-wide

            state_sixp_agg_adj = state_sixp_agg.copy()

            if slidermax != ceiling_var:
                    slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                id = "slider"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                    state_sixp_agg_adj = state_sixp_agg[state_sixp_agg['6p_total'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(state_sixp_agg_adj, geojson=states_gj, locations='state',
                                color='6p_total',
                                color_continuous_scale="Viridis",
                                range_color=(state_sixp_agg["6p_total"].min(), #count --> 6p_total
                                            state_sixp_agg["6p_total"].max()),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data=["6p_total"]
                        )

        elif border_type == "Nationwide":

            nat_dist = state_sixp_agg.copy()

            nat_val = state_sixp_agg["6p_total"].sum()
            national = [nat_val]*14
            nat_dist["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                nat_dist = nat_dist[nat_dist['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_dist, geojson=states_gj, locations='state',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data= ["National"]
                        )

    elif map_type == 'Debt Density':
        # Create county map
        # Create a new column in debt_by_county: divide number of debt holders by county population
        # Disiplay new column

        county_debt_geo['density'] = county_debt_geo['6p_total'] / county_debt_geo['population']

        density = county_debt_geo["density"]
        #x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

        state_sixp_agg['density'] = state_sixp_agg['6p_total'] / state_sixp_agg['population']

        if border_type == "Countywide":

            county_debt_geo_adj = county_debt_geo.copy()
            if slidermax != round(county_debt_geo["density"].max(), 2):
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["density"].max(), 2),
                                id = "slider"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["density"].max(), 2),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                    county_debt_geo_adj = county_debt_geo[county_debt_geo['density'].between(sliderrange[0], sliderrange[1], inclusive="both")]



            fig = px.choropleth(county_debt_geo_adj, geojson=map_gj, locations='Geo_FIPS',
                color='density',
                # color_continuous_scale="Viridis",
                range_color=(density.min(),
                        density.max()),
                featureidkey="properties.Geo_FIPS",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="county",
                hover_data=["density"],
                color_continuous_scale=[[0, 'rgb(240,240,240)'],
                    [0.1, 'rgb(126, 191, 113)'],
                    [0.2, 'rgb(91, 161, 77)'],
                    [0.75, 'rgb(227, 72, 54)'],
                    [1, 'rgb(227, 26, 28)']]
            )

        elif border_type == "Statewide":
            state_sixp_agg_adj = state_sixp_agg.copy()
            if slidermax != math.ceil(state_sixp_agg["density"].max()):  #round up. Otherwise, slider automatically rounds to 2 places
                    slider =  dcc.RangeSlider(min = 0,                # Without ceil(), it will round down, which then eliminates the max value
                                max = math.ceil(state_sixp_agg["density"].max()),
                                id = "slider"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = math.ceil(state_sixp_agg["density"].max()),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                    state_sixp_agg_adj = state_sixp_agg[state_sixp_agg['density'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(state_sixp_agg_adj, geojson=states_gj, locations='state',
                color='density',
                color_continuous_scale="Viridis",
                range_color=(state_sixp_agg['density'].min(),
                        state_sixp_agg['density'].max()),
                featureidkey="properties.state_abrev",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="state",
                hover_data=["density"]
            )

        elif border_type == "Nationwide":

            nat_dens = state_sixp_agg.copy()

            nat_val = (state_sixp_agg["6p_total"].sum())/(state_sixp_agg["population"].sum())
            national = [nat_val]*14
            nat_dens["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                nat_dens = nat_dens[nat_dens['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_dens, geojson=states_gj, locations='state',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data= ["National"]
                        )



    elif map_type == 'Average Debt Holdings':
        county_debt_geo['mean_6p_held'] = county_debt_geo['6p_total'] / county_debt_geo['count']

        six_p_tot = county_debt_geo['mean_6p_held']

        # x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

        state_sixp_agg['mean_6p_held'] = state_sixp_agg['6p_total'] / state_sixp_agg['count']

        if border_type == "Countywide":
            county_debt_geo_adj = county_debt_geo.copy()
            if slidermax != round(county_debt_geo["mean_6p_held"].max(), 2):
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["mean_6p_held"].max(), 2),
                                id = "slider"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["mean_6p_held"].max(), 2),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                    county_debt_geo_adj = county_debt_geo[county_debt_geo['mean_6p_held'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(county_debt_geo_adj, geojson=map_gj, locations='Geo_FIPS',
                color='mean_6p_held',
                # color_continuous_scale="Viridis",
                range_color=(six_p_tot.min(),
                        six_p_tot.max()),
                featureidkey="properties.Geo_FIPS",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="county",
                hover_data=["mean_6p_held"],
                color_continuous_scale=[[0, 'rgb(240,240,240)'],
                    [0.1, 'rgb(126, 191, 113)'],
                    [0.2, 'rgb(91, 161, 77)'],
                    [0.75, 'rgb(227, 72, 54)'],
                    [1, 'rgb(227, 26, 28)']]
            )

        elif border_type == "Statewide":
            state_sixp_agg_adj = state_sixp_agg.copy()
            if slidermax != round(state_sixp_agg["mean_6p_held"].max(),2):
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(state_sixp_agg["mean_6p_held"].max(), 2),
                                id = "slider"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(state_sixp_agg["mean_6p_held"].max(), 2),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                    state_sixp_agg_adj = state_sixp_agg[state_sixp_agg['mean_6p_held'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(state_sixp_agg_adj, geojson=states_gj, locations='state',
                color='mean_6p_held',
                color_continuous_scale="Viridis",
                range_color=(state_sixp_agg['mean_6p_held'].min(),
                        state_sixp_agg['mean_6p_held'].max()),
                featureidkey="properties.state_abrev",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="state",
                hover_data=["mean_6p_held"]
            )

        elif border_type == "Nationwide":

            nat_avg = state_sixp_agg.copy()

            nat_val = (state_sixp_agg["6p_total"].sum())/(state_sixp_agg["count"].sum())
            national = [nat_val]*14
            nat_avg["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider"
                                )
                nat_avg = nat_avg[nat_avg['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_avg, geojson=states_gj, locations='state',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data= ["National"]
                        )
    else:
         fig = px.choropleth()
         slider = dcc.RangeSlider(id="slider-2", min = 0, max = 10)

    return dcc.Graph(figure = fig, id = 'my-map'), [slider, 'You have selected "{}"'.format(sliderrange)]

@app.callback(
        Output('right-tab-content-2', 'children'),
        Output('range-slider-2', 'children'),
        [Input("states_drpdwn", "value"), 
        Input("county_drpdwn", "value"),
        Input('heatmap_drpdwn_2', 'value'),
        Input('border_drpdwn', 'value'),
        Input('slider-2', 'value'),
        Input('slider-2', 'max')] #to keep track of when the heatmap type changes--> means that the rangeslider maximum must be adjusted 
)
def create_new_heatmap(state, county, map_type, border_type, sliderrange, slidermax):
    global fig 

    fitbounds = False
    basemap_visible = True
    map_df_c = map_df.copy()
    state_map_df_c = state_map_df.copy()

    # save as a geojson
    map_str = map_df_c.to_json()
    map_gj = json.loads(map_str) # convert string json to dictionary json

    states_str = state_map_df_c.to_json()
    states_gj = json.loads(states_str)

    if (map_type == "Not Selected") or (map_type is None):
        return '', rangeslider2

    if (state != "All States") and (state is not None):
        if border_type == "Countywide":
            map_df_c = map_df_c.loc[map_df['state'] == state]
        if border_type == "Statewide" or border_type == "Nationwide":
            state_map_df_c = state_map_df_c.loc[state_map_df['state']==state]
        fitbounds = "locations"
        basemap_visible = False

    if (county != "All Counties") and (county is not None):
        map_df_c = map_df_c.loc[map_df_c['county'] == county]

    # save as a geojson
    map_str = map_df_c.to_json()
    map_gj = json.loads(map_str) # convert string json to dictionary json

    states_str = state_map_df_c.to_json()
    states_gj = json.loads(states_str)



    # debt info per county
    debt_by_county = pd.read_csv("../data_clean/final_data_CD.csv")[["Group State", "Group County", '6p_total']]
    debt_by_county = debt_by_county.groupby(by=["Group County", "Group State"]).agg(['size', 'sum'])
    # debt_by_county = debt_by_county.to_frame()
    # debt_by_county.rename(columns={'size':'count'}, inplace=True)
    debt_by_county.reset_index(inplace=True)

    debt_by_county.columns = debt_by_county.columns.droplevel(1)
    debt_by_county.columns = ['county', 'state', 'count', '6p_total']

    county_geo_fips = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)[["Geo_FIPS", "Geo_name", 'Geo_STUSAB', "SE_T001_001"]]
    county_geo_fips.rename(columns={"Geo_name":"county", 'Geo_STUSAB':'state', "SE_T001_001":'population'}, inplace=True)
    county_debt_geo = pd.merge(debt_by_county, county_geo_fips, on=["county", 'state'])

    state_sixp_agg = county_debt_geo.groupby('state', as_index = False).sum()
    state_sixp_agg.drop('Geo_FIPS', inplace=True, axis = 1) #the summing messes it up; also not necessary for states anyways

    if map_type == 'Population':

        # get county populations
        county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
        county_pops = county_pops[county_pops["SE_T001_001"].notna()]
        county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
        county_pops.rename(columns = {'SE_T001_001':'Population', "Geo_name":"County"}, inplace = True)
        county_pops = county_pops[["Geo_FIPS", "Population", "County"]]

        #state pop
        state_pops = gpd.read_file("../data_raw/census_data/statepop.csv")
        state_pops = state_pops[["State", "Total Pop"]].head(15)
        state_pops = state_pops.astype({"Total Pop":"int"})

        # create choropleth map based on border type
        if border_type == "Countywide":

            county_pops_adj = county_pops.copy()

            if slidermax != county_pops["Population"].max(): #when the map is loaded for the first time, maximum value will not match county_pops["Population"].max()
                slider =  dcc.RangeSlider(min = 0,
                                max = county_pops["Population"].max(),
                                id = "slider-2"
                                )
            else: #otherwise, this is the case where the map was not loaded for the first time, and the user just adjusted the rangeslider
                slider =  dcc.RangeSlider(min = 0,
                                max = county_pops["Population"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                county_pops_adj = county_pops[county_pops['Population'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(county_pops_adj, geojson=map_gj, locations='Geo_FIPS',
                    color='Population',
                    color_continuous_scale="Viridis",
                    range_color=(county_pops["Population"].min(),
                                county_pops["Population"].max()),
                    featureidkey="properties.Geo_FIPS",
                    scope="usa",
                    basemap_visible=basemap_visible,
                    fitbounds=fitbounds,
                    hover_name="County",
                    hover_data=["Population"],
                )

        elif border_type == "Statewide":

            state_pops_adj = state_pops.copy()

            if slidermax != state_pops["Total Pop"].max():
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pops["Total Pop"].max(),
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pops["Total Pop"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                state_pops_adj = state_pops[state_pops['Total Pop'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(state_pops_adj, geojson=states_gj, locations='State',
                                color='Total Pop',
                                color_continuous_scale="Viridis",
                                range_color=(state_pops["Total Pop"].min(),
                                            state_pops["Total Pop"].max()),
                                featureidkey="properties.state",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="State",
                                hover_data=["Total Pop"]
                        )

        elif border_type == "Nationwide":

            nat_pops = state_pops.copy()

            nat_val = state_pops["Total Pop"].sum()
            national = [nat_val]*15
            nat_pops["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                nat_pops = nat_pops[nat_pops['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_pops, geojson=states_gj, locations='State',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="State",
                                hover_data= ["National"]
                        )


    elif map_type == 'Slave Population':

        #basemap_visible = True
        county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
        county_pops = county_pops[county_pops["SE_T001_001"].notna()]
        county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
        county_pops.rename(columns = {'SE_T001_001':'Population', "Geo_name":"County"}, inplace = True)

        county_slaves = gpd.read_file("../data_raw/census_data/census.csv")
        county_slaves = county_slaves[["GISJOIN", "slavePopulation"]].head(290)
        county_slaves['GISJOIN'] = county_slaves['GISJOIN'].str.replace('G0', '')
        county_slaves['GISJOIN'] = county_slaves['GISJOIN'].str.replace('G', '') #convert to geo_fips
        county_slaves.rename(columns = {'GISJOIN':'Geo_FIPS'}, inplace = True)
        merged = pd.merge(county_pops, county_slaves, on=['Geo_FIPS'])
        merged = merged[["Geo_FIPS", "slavePopulation", "County"]]
        merged = merged.astype({"slavePopulation":"int", "Geo_FIPS":"str"})
        #print(merged)

        state_pop = gpd.read_file("../data_raw/census_data/statepop.csv")
        state_pop = state_pop[["State", "Slave Pop"]].head(15)
        state_pop = state_pop.astype({"Slave Pop":"int"})

        if border_type == "Countywide":
            county_slaves_adj = merged.copy()

            #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            #    print(county_slaves_adj)

            if slidermax != merged["slavePopulation"].max(): #issue with choosing state of max county
                slider =  dcc.RangeSlider(min = 0,
                                max = merged["slavePopulation"].max(),
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = merged["slavePopulation"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                county_slaves_adj = merged[merged['slavePopulation'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(county_slaves_adj, geojson=map_gj, locations='Geo_FIPS',
                    color='slavePopulation',
                    #color_continuous_scale="Viridis",
                    range_color=(merged["slavePopulation"].min(),
                                merged["slavePopulation"].max()),
                    featureidkey="properties.Geo_FIPS",
                    scope="usa",
                    basemap_visible=basemap_visible,
                    fitbounds=fitbounds,
                    hover_name="County",
                    hover_data=["slavePopulation"],
                    color_continuous_scale=[[0, 'rgb(240,240,240)'],
                            [0.1, 'rgb(126, 191, 113)'],
                            [0.2, 'rgb(91, 161, 77)'],
                            [0.75, 'rgb(227, 72, 54)'],
                            [1, 'rgb(227, 26, 28)']]
                )


        elif border_type == "Statewide":
            state_pop_adj = state_pop.copy()

            if slidermax != state_pop["Slave Pop"].max():
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pop["Slave Pop"].max(),
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = state_pop["Slave Pop"].max(),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                state_pop_adj = state_pop[state_pop['Slave Pop'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(state_pop_adj, geojson=states_gj, locations='State', #map_gj vs states_gj
                        color='Slave Pop',
                        color_continuous_scale="Viridis",
                        range_color=(state_pop['Slave Pop'].min(),
                                    state_pop['Slave Pop'].max()),
                        featureidkey="properties.state",
                        scope="usa",
                        basemap_visible=basemap_visible,
                        fitbounds=fitbounds,
                        hover_name="State",
                        hover_data=["Slave Pop"]
                    )

        elif border_type == "Nationwide":

            nat_slave = state_pop.copy()

            nat_val = state_pop["Slave Pop"].sum()
            national = [nat_val]*15
            nat_slave["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                nat_slave = nat_slave[nat_slave['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_slave, geojson=states_gj, locations='State',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="State",
                                hover_data= ["National"]
                        )

    elif map_type == 'Debt Distribution':
        # Create the debt distribution map
        # Input: archive/.../CD_geographical_table_summary.csv, countyPops.csv (GEO_FIPS column), Map geojson file
        # Create a dataframe of all county names and their GEO_FIPS code
        # Merge dataframe with CD_geographical_table_summary.csv
        # test debt distribution map
        # fig = px.choropleth()
        six_p_tot = county_debt_geo["6p_total"]

        x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

        #print(six_p_tot[six_p_tot.between(six_p_tot.quantile(.85), six_p_tot.quantile(1))])

        Q1 = np.percentile(county_debt_geo['6p_total'], 25, method='midpoint')
        Q3 = np.percentile(county_debt_geo['6p_total'], 75, method='midpoint')
        IQR = Q3 - Q1

        # Above Upper bound
        upper=Q3+1.5*IQR
        upper_array=np.array(county_debt_geo['6p_total']>=upper)

        #Below Lower bound
        lower=Q1-1.5*IQR
        lower_array=np.array(county_debt_geo['6p_total']<=lower)

        xiv = pd.Interval(x.min(), x.max())
        xmid = xiv.mid

        if border_type == "Countywide": #automatic rounding issue. See explanation in debt density section

            ceiling_var = county_debt_geo["6p_total"].max() + 1000 #so that the slider does not round down and exclude the actual max value

            county_debt_geo_adj = county_debt_geo.copy()
            if slidermax != ceiling_var:
                slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                county_debt_geo_adj = county_debt_geo[county_debt_geo['6p_total'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            print(sliderrange)

            fig = px.choropleth(county_debt_geo_adj, geojson=map_gj, locations='Geo_FIPS',
                        color='6p_total',
                        #color_continuous_scale="Viridis",
                        range_color=(county_debt_geo['6p_total'].min(),
                                    county_debt_geo['6p_total'].max()),
                        featureidkey="properties.Geo_FIPS",
                        scope="usa",
                        basemap_visible=basemap_visible,
                        fitbounds=fitbounds,
                        hover_name="county",
                        hover_data=["6p_total"],
                        color_continuous_scale=[[0, 'rgb(240,240,240)'],
                            [0.1, 'rgb(126, 191, 113)'],
                            [0.2, 'rgb(91, 161, 77)'],
                            [0.75, 'rgb(227, 72, 54)'],
                            [1, 'rgb(227, 26, 28)']]
                    )
        elif border_type == "Statewide":

            ceiling_var = state_sixp_agg["6p_total"].max() + 1000 #same reasoning as for county-wide

            state_sixp_agg_adj = state_sixp_agg.copy()

            if slidermax != ceiling_var:
                    slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                id = "slider-2"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = ceiling_var,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                    state_sixp_agg_adj = state_sixp_agg[state_sixp_agg['6p_total'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(state_sixp_agg_adj, geojson=states_gj, locations='state',
                                color='6p_total',
                                color_continuous_scale="Viridis",
                                range_color=(state_sixp_agg["6p_total"].min(), #count --> 6p_total
                                            state_sixp_agg["6p_total"].max()),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data=["6p_total"]
                        )

        elif border_type == "Nationwide":

            nat_dist = state_sixp_agg.copy()

            nat_val = state_sixp_agg["6p_total"].sum()
            national = [nat_val]*14
            nat_dist["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                nat_dist = nat_dist[nat_dist['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_dist, geojson=states_gj, locations='state',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data= ["National"]
                        )

    elif map_type == 'Debt Density':
        # Create county map
        # Create a new column in debt_by_county: divide number of debt holders by county population
        # Disiplay new column

        county_debt_geo['density'] = county_debt_geo['6p_total'] / county_debt_geo['population']

        density = county_debt_geo["density"]
        #x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

        state_sixp_agg['density'] = state_sixp_agg['6p_total'] / state_sixp_agg['population']

        if border_type == "Countywide":

            county_debt_geo_adj = county_debt_geo.copy()
            if slidermax != round(county_debt_geo["density"].max(), 2):
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["density"].max(), 2),
                                id = "slider-2"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["density"].max(), 2),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                    county_debt_geo_adj = county_debt_geo[county_debt_geo['density'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(county_debt_geo_adj, geojson=map_gj, locations='Geo_FIPS',
                color='density',
                # color_continuous_scale="Viridis",
                range_color=(density.min(),
                        density.max()),
                featureidkey="properties.Geo_FIPS",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="county",
                hover_data=["density"],
                color_continuous_scale=[[0, 'rgb(240,240,240)'],
                    [0.1, 'rgb(126, 191, 113)'],
                    [0.2, 'rgb(91, 161, 77)'],
                    [0.75, 'rgb(227, 72, 54)'],
                    [1, 'rgb(227, 26, 28)']]
            )

        elif border_type == "Statewide":
            state_sixp_agg_adj = state_sixp_agg.copy()
            if slidermax != math.ceil(state_sixp_agg["density"].max()):  #round up. Otherwise, slider automatically rounds to 2 places
                    slider =  dcc.RangeSlider(min = 0,                # Without ceil(), it will round down, which then eliminates the max value
                                max = math.ceil(state_sixp_agg["density"].max()),
                                id = "slider-2"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = math.ceil(state_sixp_agg["density"].max()),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                    state_sixp_agg_adj = state_sixp_agg[state_sixp_agg['density'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(state_sixp_agg_adj, geojson=states_gj, locations='state',
                color='density',
                color_continuous_scale="Viridis",
                range_color=(state_sixp_agg['density'].min(),
                        state_sixp_agg['density'].max()),
                featureidkey="properties.state_abrev",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="state",
                hover_data=["density"]
            )

        elif border_type == "Nationwide":

            nat_dens = state_sixp_agg.copy()

            nat_val = (state_sixp_agg["6p_total"].sum())/(state_sixp_agg["population"].sum())
            national = [nat_val]*14
            nat_dens["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                nat_dens = nat_dens[nat_dens['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_dens, geojson=states_gj, locations='state',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data= ["National"]
                        )



    elif map_type == 'Average Debt Holdings':
        county_debt_geo['mean_6p_held'] = county_debt_geo['6p_total'] / county_debt_geo['count']

        six_p_tot = county_debt_geo['mean_6p_held']

        # x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

        state_sixp_agg['mean_6p_held'] = state_sixp_agg['6p_total'] / state_sixp_agg['count']

        if border_type == "Countywide":
            county_debt_geo_adj = county_debt_geo.copy()
            if slidermax != round(county_debt_geo["mean_6p_held"].max(), 2):
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["mean_6p_held"].max(), 2),
                                id = "slider-2"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(county_debt_geo["mean_6p_held"].max(), 2),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                    county_debt_geo_adj = county_debt_geo[county_debt_geo['mean_6p_held'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(county_debt_geo_adj, geojson=map_gj, locations='Geo_FIPS',
                color='mean_6p_held',
                # color_continuous_scale="Viridis",
                range_color=(six_p_tot.min(),
                        six_p_tot.max()),
                featureidkey="properties.Geo_FIPS",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="county",
                hover_data=["mean_6p_held"],
                color_continuous_scale=[[0, 'rgb(240,240,240)'],
                    [0.1, 'rgb(126, 191, 113)'],
                    [0.2, 'rgb(91, 161, 77)'],
                    [0.75, 'rgb(227, 72, 54)'],
                    [1, 'rgb(227, 26, 28)']]
            )

        elif border_type == "Statewide":
            state_sixp_agg_adj = state_sixp_agg.copy()
            if slidermax != round(state_sixp_agg["mean_6p_held"].max(),2):
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(state_sixp_agg["mean_6p_held"].max(), 2),
                                id = "slider-2"
                                )
            else:
                    slider =  dcc.RangeSlider(min = 0,
                                max = round(state_sixp_agg["mean_6p_held"].max(), 2),
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                    state_sixp_agg_adj = state_sixp_agg[state_sixp_agg['mean_6p_held'].between(sliderrange[0], sliderrange[1], inclusive="both")]


            fig = px.choropleth(state_sixp_agg_adj, geojson=states_gj, locations='state',
                color='mean_6p_held',
                color_continuous_scale="Viridis",
                range_color=(state_sixp_agg['mean_6p_held'].min(),
                        state_sixp_agg['mean_6p_held'].max()),
                featureidkey="properties.state_abrev",
                scope="usa",
                basemap_visible=basemap_visible,
                fitbounds=fitbounds,
                hover_name="state",
                hover_data=["mean_6p_held"]
            )

        elif border_type == "Nationwide":

            nat_avg = state_sixp_agg.copy()

            nat_val = (state_sixp_agg["6p_total"].sum())/(state_sixp_agg["count"].sum())
            national = [nat_val]*14
            nat_avg["National"] = national

            if slidermax != nat_val:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                id = "slider-2"
                                )
            else:
                slider =  dcc.RangeSlider(min = 0,
                                max = nat_val,
                                value=[sliderrange[0], sliderrange[1]],
                                id = "slider-2"
                                )
                nat_avg = nat_avg[nat_avg['National'].between(sliderrange[0], sliderrange[1], inclusive="both")]

            fig = px.choropleth(nat_avg, geojson=states_gj, locations='state',
                                color='National',
                                color_continuous_scale="Viridis",
                                range_color=(0, nat_val),
                                featureidkey="properties.state_abrev",
                                scope="usa",
                                basemap_visible=basemap_visible,
                                fitbounds=fitbounds,
                                hover_name="state",
                                hover_data= ["National"]
                        )

    else:
         fig = px.choropleth()
         slider = dcc.RangeSlider(id="slider-2", min = 0, max = 10)

    return dcc.Graph(figure=fig, id='my-map-2'), [slider, 'You have selected "{}"'.format(sliderrange)]

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
    html.Div(className='tabs-container', children=[left_tab, right_tab]),
    html.Div(className='right-tab', children=display_tab),
    # html.Div(className='right-tab-2', children=right_tab_2)
])

# run app
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
