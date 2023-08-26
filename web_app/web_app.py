# import packages
import json
import math

import dash
import dash_bootstrap_components as dbc
import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import time
from shapely import wkt

# import json file that converts full name of a state to two character abbreviation
with open('assets/state_codes.json', "r") as file:
    state_codes = json.load(file)
state_codes_inv = {v: k for k, v in state_codes.items()}

########################################################################################################################
###################################### dataframes used for maps ########################################################
########################################################################################################################
# data for counties is preprocessed elsewhere, saves us 3s
df_raw = pd.read_csv('assets/map_df.csv', index_col = 0)
df_raw['geometry'] = df_raw['geometry'].apply(wkt.loads)
map_df = gpd.GeoDataFrame(df_raw)


# only contains state borders, no county borders
# don't optimize time because it's fast enough without optimizing 
state_map_df = gpd.read_file("../data_raw/shapefiles/stateshape_1790")
state_map_df.rename(columns={'STATENAM': 'state'}, inplace=True)
state_map_df['state_abrev'] = state_map_df.loc[:, 'state']
state_map_df.replace({"state_abrev": state_codes}, inplace=True)

# list of states we include in dropdown menu
states = pd.read_csv("../data_raw/census_data/statepop.csv")["State"].dropna()
states = pd.concat([pd.Series(["All States"]), states]).tolist()
# remove states that have no map data
states.remove("Maine")
states.remove("Kentucky")
states.remove("Tennessee")

########################################################################################################################
###################################### dataframes used for maps ########################################################
########################################################################################################################
# DEBT - COUNTY + STATE LEVEL
# county - import debt
debt_by_county = pd.read_csv("../data_clean/final_data_CD.csv")[["Group State", "Group County", '6p_total']]
debt_by_county = debt_by_county.groupby(by=["Group County", "Group State"]).agg(['size', 'sum'])
debt_by_county.reset_index(inplace=True)
debt_by_county.columns = debt_by_county.columns.droplevel(1)
debt_by_county.columns = ['county', 'state', 'count', '6p_total']
# county - import geography and population data
county_pop_data_raw = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
county_geo_fips = county_pop_data_raw[county_pop_data_raw["SE_T001_001"].notna()]
county_geo_fips = county_geo_fips.astype({"SE_T001_001": "int", "Geo_FIPS": "str"})
county_geo_fips = county_geo_fips[["Geo_FIPS", "Geo_name", 'Geo_STUSAB', "SE_T001_001"]]
county_geo_fips.rename(columns={"Geo_name": "county", 'Geo_STUSAB': 'state', "SE_T001_001": 'population'},
                       inplace=True)
county_debt_geo = pd.merge(debt_by_county, county_geo_fips, on=["county", 'state'])
county_debt_geo['density'] = county_debt_geo['6p_total'] / county_debt_geo['population']
county_debt_geo['mean_6p_total'] = county_debt_geo['6p_total']/county_debt_geo['count']
# state
state_debt_geo = county_debt_geo.groupby('state', as_index=False).sum()
state_debt_geo['state'] = state_debt_geo['state'].apply(lambda x: state_codes_inv[x])
state_debt_geo['density'] = state_debt_geo['6p_total'] / state_debt_geo['population']
state_debt_geo['mean_6p_total'] = state_debt_geo['6p_total']/county_debt_geo['count']
# national
nat_debt_geo = state_debt_geo.copy()
nat_debt_geo['count'] = nat_debt_geo['count'].sum()
nat_debt_geo['6p_total'] = nat_debt_geo['6p_total'].sum()
nat_debt_geo['population'] = nat_debt_geo['population'].sum()
nat_debt_geo["density"] = state_debt_geo['6p_total'].sum()/state_debt_geo["population"].sum()
nat_debt_geo["mean_6p_total"] = state_debt_geo['6p_total'].sum()/state_debt_geo["count"].sum()

# SLAVE POPULATION - COUNTY + STATE LEVEL
# county
county_slaves = gpd.read_file("../data_raw/census_data/census.csv")
county_slaves = county_slaves[["GISJOIN", "slavePopulation"]].head(290)
county_slaves['GISJOIN'] = county_slaves['GISJOIN'].str.replace('G0', '')
county_slaves['GISJOIN'] = county_slaves['GISJOIN'].str.replace('G', '')  # convert to geo_fips
county_slaves.rename(columns={'GISJOIN': 'Geo_FIPS'}, inplace=True)
county_slaves_data = pd.merge(county_geo_fips, county_slaves, on=['Geo_FIPS'])
county_slaves_data = county_slaves_data.astype({"slavePopulation": "int", "Geo_FIPS": "str"})
# state
state_slaves_data = county_slaves_data.groupby('state')['slavePopulation'].sum().reset_index()
state_slaves_data['state'] = state_slaves_data['state'].apply(lambda x: state_codes_inv[x])
# national
nat_slaves_data = state_slaves_data.copy()
nat_slaves_data["slavePopulation"] = state_slaves_data["slavePopulation"].sum()

# create final dataset
county_data_final = pd.merge(county_slaves_data, county_debt_geo, how = 'outer')
state_data_final = pd.merge(state_slaves_data, state_debt_geo, how = 'outer')
national_data_final = pd.merge(nat_slaves_data, nat_debt_geo, how = 'outer')

# MAP from parameter option to column
map_to_col = {'Population': 'population',
              'Slave Population': 'slavePopulation',
              'Debt Distribution': '6p_total',
              'Debt Density': 'density',
              'Average Debt Holdings': 'debt density'}


########################################################################################################################
######################################### Define App Components ########################################################
########################################################################################################################
# create web app, import bootstrap stylesheet + external stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'], \
                suppress_callback_exceptions=True)

# Title Bar
title = html.H1(children='American National Debt in the Late 18th Century', style={'textAlign': 'left'}, className='title')

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


# Left tab with map options
left_tab = html.Div(id="left_tab", className='box', children=[
    html.H3(children='Customize', className='box-title', style={'textAlign': 'center'}),
    html.Div(id="regions_c_drpdwn", children=[
        html.H5(
            children=["Region", html.Button(children='ℹ', className='more_info_btn', id='more_info_regions', n_clicks=0)]),
        dcc.Dropdown(
            id="reg_drpdwn",
            options=['Not Selected', 'Nation', 'State', 'County'],
            value='Not Selected'
        ),
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
                dbc.ModalBody(
                    "Statistic determines what metric the map displays. For example, Population shows you, at each unit" + \
                    " of your border, the population.")
            ],
            id='heatmap_modal'
        )

    ], style={"display": "block"}),
    html.Div(id="states_c_drpdwn", children=[
        dcc.Dropdown(id="states_drpdwn", style={"display": "none", 'padding-top': '25%'})
    ]),
    html.Div(id="c_drpdwn", children=[
        dcc.Dropdown(id="county_drpdwn", style={"display": "none", 'padding-top': '25%'})
    ]),
    html.Div(id="bord_c_drpdwn", children=[
        dcc.Dropdown(id="border_drpdwn", style={"display": "none"}),
    ]),
    html.Div(id="heatmap_c_drpdwn", children=[
        dcc.Dropdown(id="heatmap_drpdwn", style={"display": "none"}),
    ]),
], style={'width': '35%', 'height': 'auto', "display": "block"})

# right tab to show statistics associated with that particular geographical area
right_tab = html.Div(id="right_tab", className='box', children=[
    html.H3(children='Statistics', className='box-title', style={'textAlign': 'center'}),
], style={'width': '65%', 'height': 'auto', "display": "block"})

# Bottom Display tab with DataFrame/Map
display_tab = html.Div(className='box', children=[
    html.H3(children='Display', className='box-title', style={'textAlign': 'center'}),
    html.Div(id='right-tab-content',
             style={'overflow': 'scroll'}
             ),
    html.Div(id="range-slider", children=[
        dcc.RangeSlider(id="slider", min=0, max=10)
    ], style={"display": "none"})
], style={'width': '100%', 'height': '85vh'})

########################################################################################################################
########################################### Helper Functions ###########################################################
########################################################################################################################
def returnSlider(df, col, slidermax, sliderrange):
    maxval = df[col].max()+1
    if slidermax != maxval:
        slider = dcc.RangeSlider(min=0, max=maxval, id="slider")
        return df, slider
    else:
        slider = dcc.RangeSlider(min=0, max=maxval, value=[sliderrange[0], sliderrange[1]], id="slider")
        df_adj = df[df[col].between(sliderrange[0], sliderrange[1], inclusive="both")]
        return df_adj, slider

def returnFig(df_adj, df_geojson, geo_col, color_col, featureidkey, basemap_visible, fitbounds, hover_name, hover_data):
    fig = px.choropleth(
        df_adj, geojson=df_geojson, locations=geo_col, color=color_col, color_continuous_scale="Viridis",
        range_color=(df_adj[color_col].min(), df_adj[color_col].max()), featureidkey=featureidkey,
        scope="usa", basemap_visible=basemap_visible, fitbounds=fitbounds, hover_name=hover_name, hover_data=[hover_data])
    return fig
########################################################################################################################
######################################### Callback Functions ###########################################################
########################################################################################################################
# Callback function to display range slider when heatmap type is chosen
@app.callback(
    Output("range-slider", "style"),
    [Input("heatmap_drpdwn", "value")]
)
def add_range_slider(stat_val):
    """
    chooses to display or hide the dropdown menu
    :param stat_val: what parameter was selected for the Statistic option
    :return: display style - show or hide
    """
    if (stat_val is not None) and (stat_val != "Not Selected"):
        return {"display": "block"}
    else:
        return {"display": "none"}

# when state/county is chosen as the region, display state dropdown
@app.callback(
    Output("states_c_drpdwn", "children"),
    Input("reg_drpdwn", "value")
)
def display_state_drpdwn(reg_val):
    """
    chooses what state dropdown type to show
    :param reg_val: what parameter was selected for the Region option
    :return: dropdown that the user can use to select a state
    """
    if reg_val == "State":
        state_drpdwn_title = html.H5(children="State", id="state_drpdwn_t",
                                     style={'text-align':'left'})
    elif reg_val == 'County':
        state_drpdwn_title = html.H5(children="State", id="state_drpdwn_t",
                                     style={'text-align':'left'})
    else:
        return ''
    state_drp = dcc.Dropdown(
        id="states_drpdwn",
        options=states,
        value=states[0],
        style={'width': '100%', 'align-items': 'right', 'justify-content': 'right', 'float': 'right'}
    )
    return dbc.Row([dbc.Col(state_drpdwn_title, width = 4), dbc.Col(state_drp, width = 8)], style = {'padding-top': '10px'})

#
# when state of the county is chosen, display county dropdown
@app.callback(
    Output("c_drpdwn", "children"),
    [Input("states_drpdwn", "value"),
     Input('reg_drpdwn', 'value')]
)
def display_county_drpdwn(state_val, reg_val):
    """
    display list of counties in dropdown for the user to pick from
    :param state_val: which state the user selected
    :return: dropdown with list of counties
    """
    if (state_val != "All States") and (state_val is not None) and (reg_val == 'County'):
        counties = map_df.query("state==" + "'" + state_val + "'")["county"].tolist()
        counties.insert(0, "All Counties")
        county_drpdwn_title = html.H5(children="County", id="county_drpdwn_t",
                                      style={'text-align':'left'})
        county_drp = dcc.Dropdown(
            id="county_drpdwn",
            options=counties,
            value=counties[0],
            style={'width': '100%', 'align-items': 'right', 'justify-content': 'right', 'float': 'right'}
        )
        return dbc.Row([dbc.Col(county_drpdwn_title, width = 4), dbc.Col(county_drp, width = 8)], style = {'padding-top': '10px'})
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
    """
    determines what border options are made available, given the selection of region, state and county
    :param reg_value: what region type we're displaying (county, state, nation)
    :param state_value: state
    :param county_value: county
    :return: approrpiate dropdown list
    """
    if (reg_value != "Not Selected") and (reg_value is not None):
        if (reg_value == "State") and (state_value == "All States") or (reg_value == "County") and (
                state_value == "All States") \
                or (reg_value == "County") and (county_value == "All Counties"):
            return ''
        bord_drpdwn_title = html.H5(
            children=["Border", html.Button(children="ℹ", className='more_info_btn', id="more_info_border_button")],
            id="bord_drpdwn_t")
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

# when border is chosen, display heatmap dropdown
@app.callback(
    Output("heatmap_c_drpdwn", "children"),
    [Input("border_drpdwn", "value"),  # need more input so it doesnt show up in county/state ex
     Input("reg_drpdwn", "value")]
)
def display_heatmap_drpdwn(border_value, region_value):
    if (border_value != "Not Selected") and (border_value is not None):
        heatmap_chklist_title = html.H5(
            children=["Statistic", html.Button(children='ℹ', className='more_info_btn', id='heatmap_more_info_button')],
            id="heatmap_drpdwn_t")
        heatmap_drp = dcc.Dropdown(
            id="heatmap_drpdwn",
            options=['Not Selected', 'Population', 'Slave Population', 'Debt Density', 'Debt Distribution',
                     'Average Debt Holdings'],
            value="Not Selected"
        )
        return heatmap_chklist_title, heatmap_drp
    else:
        return ''

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
     Input('slider', 'max')]
    # to keep track of when the heatmap type changes--> means that the rangeslider maximum must be adjusted
)
def handle_state_dropdown(state, county, map_type, border_type, sliderrange, slidermax):
    global fig
    global county_pop_data
    global state_pop_data
    global nat_debt

    fitbounds = "locations"
    basemap_visible = True
    map_df_c = map_df.copy()
    state_map_df_c = state_map_df.copy()

    # don't return anything if no options have been selected
    if (map_type == "Not Selected") or (map_type is None):
        return '', ''

    if (state != "All States") and (state is not None):
        if border_type == "Statewide" or border_type == "Nationwide":
            state_map_df_c = state_map_df_c.loc[state_map_df['state'] == state]
        fitbounds = "locations"
        basemap_visible = False

    if (county != "All Counties") and (county is not None):
        map_df_c = map_df_c.loc[map_df_c['county'] == county]

    # save as a geojson
    map_str = map_df_c.to_json()
    map_gj = json.loads(map_str)  # convert string json to dictionary json
    states_str = state_map_df_c.to_json()
    states_gj = json.loads(states_str)

    param = map_to_col.get(map_type, "NONE")
    if param == "NONE":
        fig = px.choropleth()
        slider = dcc.RangeSlider(id="slider", min=0, max=10)
    else:
        if border_type == "Countywide":
            county_data_final_adj, slider = returnSlider(county_data_final, param, slidermax, sliderrange)
            fig = returnFig(
                county_data_final_adj, map_gj, 'Geo_FIPS', param, 'properties.Geo_FIPS', basemap_visible, fitbounds,
                'county', param)
        elif border_type == "Statewide":
            state_data_final_adj, slider = returnSlider(state_data_final, param, slidermax, sliderrange)
            fig = returnFig(
                state_data_final_adj, states_gj, 'state', param, 'properties.state', basemap_visible, fitbounds,
                'state', param)
        elif border_type == "Nationwide":
            national_data_final_adj, slider = returnSlider(national_data_final, param, slidermax, sliderrange)
            fig = returnFig(
                national_data_final_adj, states_gj, 'state', 'population', 'properties.state', basemap_visible, fitbounds,
                'state', "population")

    return dcc.Graph(figure=fig, id='my-map', style={'height':'70vh'}), [slider, 'You have selected {}'.format(sliderrange)]


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
