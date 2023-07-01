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
import json
import os
import matplotlib.pyplot as plt 
import numpy as np

state_codes = {
    "New Hampshire":"NH",
    "Vermont":"VT",
    "Rhode Island":"RI",
    "Connecticut":"CT",
    "New York":"NY",
    "New Jersey":"NJ",
    "Pennsylvania":"PA",
    "Delaware":"DE",
    "Maryland":"MD",
    "Virginia":"VA",
    "North Carolina":"NC",
    "South Carolina":"SC",
    "Georgia":"GA",
    "Massachusetts":"MA"
}

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

map_ops = dcc.Dropdown(id="st_checklist", options=["Total State Population", "Total Slave Population", 
                                 "Total Number of Debt Holders", "Percentage Debt Holders Nationally", 
                                 "Total Amount of Debt", "Percentage of Total National Debt", "Occupations with Most Debt"], 
                        value=["Total State Population"], multi=True)

# county options
c_ops = dcc.Dropdown(id="c_checklist", options=["Total County Population", "Total Number of Debt Holders", 
                                                 "Percentage of Debt Holders (Statewide)", "Total Amount of Debt", 
                                                 "Percentage of Total Debt (Statewide)"], 
                        value=["Total County Population"], multi=True)

# title: "display options"
disp_op_title = html.H5(children="Display Options (State)", id="disp_op_title")
# title: "map options"
map_op_title = html.H5(children="State Options", id="map_op_title")
# title: "county options"
c_op_title = html.H5(children="County Options", id="c_op_title")

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
# title : "county information"
c_info_title = html.H5(children="County Info")
# title : "town information"
t_info_title = html.H5(children="Town Info")

# display options checklist: choose what to display 
disp_ops_checklist = dcc.Checklist(id="disp_ops_checklist", options=[
    "Hide Choose a State", 
    "Hide State Options", 
    "Hide State Info" 
])

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
            labelStyle={'display':'block'}
        ),
        html.Br(),
        dcc.RadioItems(
           id="map_type_ops",
           options=[
               {'label':'Population', 'value':'population'},
               {'label':'Debt Distribution', 'value':'debt dist'},
               {'label':'Slave Population', 'value':'slavery'}
           ],
           value='population',
           labelStyle={"display":"block"}
       ) 
    ]), 
    html.Div(id="display_ops", children=[
        disp_op_title,
        disp_ops_checklist
    ]), 
    html.Div(id="st_c_drpdwn", children=[
        st_title,
        states_drp 
    ], style={"display":"block"}), 
    html.Div(id="state_ops", children=[
        map_op_title,
        map_ops
    ], style={"display":"block"}), 
    html.Div(id="st_info", children=[
        st_info_title,
        html.Ul(id="st_infolist")
    ]), 
    html.Div(id="c_drpdwn", children=[
        dcc.Dropdown(id="county_drpdwn", style={"display":"none"})
    ]), 
    html.Div(id="c_ops", children=[
        c_op_title,
        c_ops 
    ], style={"display":"none"}),
    html.Div(id="c_info", children=[
        c_info_title, 
        html.Ul(id="c_infolist")
    ]), 
    html.Div(id="t_drpdwn", children=[
        dcc.Dropdown(id="towns_drpdwn", style={"display":"none"})
    ], style={"display":"block"}), 
    html.Div(id="t_ops", children=[
        dcc.Checklist(id="t_checklist", style={"display":"none"})
    ]),
    html.Div(id="t_info", children=[
        t_info_title, 
        html.Ul(id="t_infolist"),
    ])
], style={'width': '40%', 'height': 'auto', "display":"block"})

# Right tab with DataFrame/Map
right_tab = html.Div(className='box', children=[
    html.H3(children='Display', className='box-title', style={'textAlign': 'center'}),
    html.Div(id='right-tab-content', 
                style={'overflow': 'scroll'}
             )
], style={'width': '60%', 'height': '600px'})

# check if a display option is selected 
# edit layout accordingly 
@app.callback(
        [Output("st_c_drpdwn", "style", allow_duplicate=True), 
         Output("state_ops", "style", allow_duplicate=True), 
         Output("st_info", "style", allow_duplicate=True)],
        [Input("disp_ops_checklist", "value")],
        prevent_initial_call=True
)

def handle_st_disp_ops(options):
    new_display_ops = [{"display":"block"}, {"display":"block"}, {"display":"block"}]
    for option in options:
        if option == "Hide Choose a State": 
            new_display_ops[0] = {"display":"none"}
        elif option == "Hide State Options":
            new_display_ops[1] = {"display":"none"}
        elif option == "Hide State Info":
            new_display_ops[2] = {"display":"none"}

    return new_display_ops

# check if town option is selected
# for each town option, display necessary information 
@app.callback(
        Output("t_infolist", "children"),
        [Input("t_checklist", "value"), 
         Input("states_drpdwn", "value"),
         Input("county_drpdwn", "value"),
         Input("towns_drpdwn", "value")]
)
def handle_t_ops(options, sel_state, sel_county, sel_town):
    display_items = []

    if sel_state != "All States" and sel_county != "Not Selected" and sel_town != None:
        towns_pops = pd.read_csv("../data_clean/Ancestry_Web_Scraper/town_pops_clean.csv")
        town_pop_df = towns_pops.loc[(towns_pops["city"] == sel_town) & (towns_pops["county"] == sel_county) & 
                                    (towns_pops["state"] == sel_state), "population"]
        town_pop = town_pop_df.iloc[0]
        for option in options:
            if option == "Total Town Population":
                display_items.append(html.Li(children=[html.B(children="Total Town Population"), ": " + str(town_pop)]))
            elif option == "Percentage of Town Holding Debt" and town_pop != "NR":
                final_cd_df = pd.read_csv("../data_clean/final_data_CD.csv") 
                total_t_holders = len(final_cd_df.loc[(final_cd_df["Group State"] == state_codes[sel_state]) & (final_cd_df["Group County"] == sel_county + " County")
                                                    & (final_cd_df["Group Town"] == sel_town)])
                display_items.append(html.Li(children=[html.B(children="Percentage of Town Holding Debt"), ": " + str(round(total_t_holders / float(town_pop), 2) * 100) + "%"]))

    return display_items

# check if town is selected
# if town is selected, display town options 
@app.callback(
        Output("t_ops", "children"), 
        Input("towns_drpdwn", "value")  
)
def display_t_ops(town):
    if town != None:
        t_op_title = html.H5(children="Town Options")
        t_checklist = dcc.Dropdown(
            id="t_checklist",
            options=[
                "Total Town Population",
                "Percentage of Town Holding Debt"
            ],
            value=["Total Town Population"],
            multi=True
        )
        return t_op_title, t_checklist 
    else:
        return ''

# check if county is selected 
# get list of towns in the county 
# display dropdown in id=t_drpdwn 
@app.callback(
        Output("t_drpdwn", "children"), 
        [Input("county_drpdwn", "value"), 
         Input("states_drpdwn", "value")]
)
def display_t_drpdwn(sel_county, sel_state):
    if sel_county != "Not Selected":
        towns_pops = pd.read_csv("../data_clean/Ancestry_Web_Scraper/town_pops_clean.csv")
        towns_l = towns_pops.loc[(towns_pops["county"] == sel_county) & (towns_pops["state"] == sel_state), "city"].tolist()
        t_drpdwn = dcc.Dropdown(
            id="towns_drpdwn",
            options=towns_l
        )
        t_title = html.H5(children="Pick a Town") 
        return t_title, t_drpdwn 
    else: 
        return ''

# get checked box values 
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

    if sel_state != "All States":
        final_cd_df = pd.read_csv("../data_clean/final_data_CD.csv")
        
        for option in options:
            if option == "Total State Population":
                tot_st_pop = state_pops.loc[state_pops["State"] == sel_state, "Total Pop"].iloc[0]
                display_items.append(html.Li(children=[html.B(children="Total State Population"), ": " + str(tot_st_pop)]))
            elif option == "Total Slave Population":
                tot_sl_pop = state_pops.loc[state_pops["State"] == sel_state, "Slave Pop"].iloc[0]
                display_items.append(html.Li(children=[html.B(children="Total Slave Population"), ": " + str(tot_sl_pop)]))
            elif option == "Total Number of Debt Holders":
                debt_holder_st = final_cd_df.loc[final_cd_df["Group State"] == state_codes[sel_state]] 
                total_num_holders = len(debt_holder_st) 
                display_items.append(html.Li(children=[html.B(children="Total Number of Debt Holders"), ": " + str(total_num_holders)]))
            elif option == "Percentage Debt Holders Nationally":
                total_cd_df = len(final_cd_df) 
                debt_holder_st = final_cd_df.loc[final_cd_df["Group State"] == state_codes[sel_state]] 
                total_num_holders = len(debt_holder_st) 
                display_items.append(html.Li(children=[html.B(children="Percentage of Debt Holders Nationally"), ": " + str(round((total_num_holders / total_cd_df) * 100, 3)) + "%"]))
            elif option == "Total Amount of Debt":
                total_debt_st = final_cd_df.loc[final_cd_df["Group State"] == state_codes[sel_state], "final_total"].sum()
                display_items.append(html.Li(children=[html.B(children="Total Amount of Debt"), ": " + str(round(total_debt_st, 2))]))
            elif option == "Percentage of Total National Debt":
                total_debt_col = final_cd_df["final_total"].sum()
                total_debt_st = final_cd_df.loc[final_cd_df["Group State"] == state_codes[sel_state], "final_total"].sum()
                display_items.append(html.Li(children=[html.B(children="Percentage of Total National Debt"), ": " + str(round((total_debt_st / total_debt_col) * 100, 3)) + "%"]))
            elif option == "Occupations with Most Debt": 
                occ_exists = os.path.isfile("../archive/S2022/occupational_analysis/avg_debt_occupation/FinishedSpreadsheets/Occupations" 
                                            + state_codes[sel_state] + ".csv") # check if occupations data exists for that state
                if occ_exists:
                    occ_data_st = pd.read_csv("../archive/S2022/occupational_analysis/avg_debt_occupation/FinishedSpreadsheets/Occupations" 
                                            + state_codes[sel_state] + ".csv")
                    occs = occ_data_st["occupation"].tolist()
                    occ_list = ["Occupations with the Most Debt (up to 5)"]
                    if len(occs) > 5:
                        i = 0
                        while i < 5:
                            occ_list.append(html.Li(occs[i]))
                            i += 1; 
                    else:
                        for occ in occs:
                            occ_list.append(html.Li(occ)) 
                    
                    display_items.append(html.Ul(html.B(children=occ_list)))
                else:
                    display_items.append(html.Li(html.Ul(children="No occupation data available for " + sel_state)))

    return display_items

# handle county options 
# display county info as a list
@app.callback(
        Output("c_infolist", "children"), 
        [Input("c_checklist", "value"), 
        Input("states_drpdwn", "value"),
        Input("county_drpdwn", "value")]
)
def handle_c_ops(options, sel_state, sel_county):
    display_items = []
    final_cd_df = pd.read_csv("../data_clean/final_data_CD.csv") 
    if sel_state != "All States" and sel_county != "Not Selected":
        for option in options:
            if option == "Total County Population":
                county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
                county_pops.rename(columns={"Geo_STUSAB":"state", "Geo_NHGISNAM":"county"}, inplace=True)
                c_pop = county_pops.loc[(county_pops["state"] == state_codes[sel_state]) & (county_pops["county"] == sel_county), "SE_T001_001"].iloc[0]
                display_items.append(html.Li(children=[html.B(children="Total County Population"), ": " + str(c_pop)]))
            elif option == "Total Number of Debt Holders":
                total_c_holders = len(final_cd_df.loc[(final_cd_df["Group State"] == state_codes[sel_state]) & (final_cd_df["Group County"] == sel_county + " County")])
                display_items.append(html.Li(children=[html.B(children="Total Number of Debt Holders"), ": " + str(total_c_holders)]))
            elif option == "Percentage of Debt Holders (Statewide)":
                total_st_holders = len(final_cd_df.loc[final_cd_df["Group State"] == state_codes[sel_state]])
                total_c_holders = len(final_cd_df.loc[(final_cd_df["Group State"] == state_codes[sel_state]) & (final_cd_df["Group County"] == sel_county + " County")])
                display_items.append(html.Li(children=[html.B(children="Percentage of Debt Holders (Statewide)"), ": " + str(round(total_c_holders / total_st_holders, 3) * 100) + "%"]))
            elif option == "Total Amount of Debt":
                total_c_debt = final_cd_df.loc[(final_cd_df["Group State"] == state_codes[sel_state]) & (final_cd_df["Group County"] == sel_county + " County"), "final_total"].sum()
                display_items.append(html.Li(children=[html.B(children="Total Amount of Debt in County"), ": " + str(round(total_c_debt, 2))]))
            elif option == "Percentage of Total Debt (Statewide)":
                total_st_debt = final_cd_df.loc[final_cd_df["Group State"] == state_codes[sel_state], "final_total"].sum()
                total_c_debt = final_cd_df.loc[(final_cd_df["Group State"] == state_codes[sel_state]) & (final_cd_df["Group County"] == sel_county + " County"), "final_total"].sum()
                display_items.append(html.Li(children=[html.B(children="Percentage of Total Debt (Statewide)"), ": " + str(round(total_c_debt / total_st_debt, 3) * 100) + "%"]))

    return display_items 

#display county options when a county is chosen
# st_info, c_info, t_ops, t_drpdwn, t_info
@app.callback(
        [Output("c_ops", "style"),
         Output("c_info", "style"),
         Output("st_info", "style"), 
         Output("t_ops", "style"),
         Output("t_drpdwn", "style"),
         Output("t_info", "style"),
         Output("display_ops", "style")],
        [Input("states_drpdwn", "value"),
         Input("left-tab-options", "value")]
)
def add_c_options(sel_state, value):
    if value == "map" and sel_state != "All States":
        return {"display":"block"}, {"display":"block"}, {"display":"block"}, {"display":"block"}, {"display":"block"}, {"display":"block"}, {"display":"block"}
    else:
        return {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}

# call back function to display dropdown menus when 'map' is clicked
@app.callback( 
        [Output("st_c_drpdwn", "style"),
         Output("c_drpdwn", "style"),
         Output('map_type_ops', 'labelStyle')],
        Input("left-tab-options", "value")
)
def add_map_options(value):
    if value == "map":
        return {"display":"block"}, {"display":"block"}, {"display":"block"}
    else:
        return {"display":"none"}, {"display":"none"}, {"display":"none"}

# call back function to display map options when 'a state' is clicked 
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
         Input("county_drpdwn", "value"),
        Input("left-tab-options", "value"), 
        Input('map_type_ops', 'value')] 
)

def handle_state_dropdown(state, county, option, map_type):
    if option == "map":
        fitbounds = False
        basemap_visible = True
        map_df_c = map_df.copy()

        if (state != "All States" and state != None):
            map_df_c = map_df_c.loc[map_df['state'] == state]
            fitbounds = "locations"
            basemap_visible = False

        if (county != "Not Selected" and county != None):
            map_df_c = map_df_c.loc[map_df_c['county'] == county]

        # save as a geojson
        map_str = map_df_c.to_json()
        map_gj = json.loads(map_str) # convert string json to dictionary json 

        if map_type == 'population':

            # get county populations 
            county_pops = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)
            county_pops = county_pops[county_pops["SE_T001_001"].notna()]
            county_pops = county_pops.astype({"SE_T001_001":"int", "Geo_FIPS":"str"})
            county_pops.rename(columns = {'SE_T001_001':'Population', "Geo_name":"County"}, inplace = True)
            county_pops = county_pops[["Geo_FIPS", "Population", "County"]]

            # create choropleth map 
            fig = px.choropleth(county_pops, geojson=map_gj, locations='Geo_FIPS', 
                                    color='Population',
                                    color_continuous_scale="Viridis",
                                    range_color=(county_pops["Population"].min(), 
                                                county_pops["Population"].max()),
                                    featureidkey="properties.Geo_FIPS",
                                    scope="usa",
                                    basemap_visible=basemap_visible,
                                    fitbounds=fitbounds,
                                    hover_name="County",
                                    hover_data=["Population"]
                                )
            slider =  dcc.RangeSlider(min = county_pops["Population"].min(), 
                                      max = county_pops["Population"].max(), 
                                      step= 10000, 
                                      value=[county_pops["Population"].min(), county_pops["Population"].max()],
                                      id = "my-rangeslider"
                                     )
        elif map_type == 'slavery':
            
            basemap_visible = True

            state_pop = gpd.read_file("../data_raw/census_data/statepop.csv")
            state_pop = state_pop[["State", "Slave Pop"]].head(15)
            state_pop.replace({"State": state_codes}, inplace = True)
            state_pop = state_pop.astype({"Slave Pop":"int"})

            fig = px.choropleth(state_pop, geojson=map_gj, locations='State', 
                            locationmode='USA-states',
                            color='Slave Pop',
                            color_continuous_scale="Viridis",
                            range_color=(state_pop['Slave Pop'].min(), 
                                        state_pop['Slave Pop'].max()),
                            featureidkey="properties.State",
                            scope="usa",
                            basemap_visible=basemap_visible,
                            fitbounds=fitbounds,
                            hover_name="State",
                            hover_data=["Slave Pop"]
                        )   
            slider =  dcc.RangeSlider(0, 20, value=[5, 15])

        elif map_type == 'debt dist':
            # Create the debt distribution map
            # Input: archive/.../CD_geographical_table_summary.csv, countyPops.csv (GEO_FIPS column), Map geojson file 
            # Create a dataframe of all county names and their GEO_FIPS code 
            # Merge dataframe with CD_geographical_table_summary.csv 
            basemap_visible = True

            debt_by_county = pd.read_csv("../data_clean/final_data_CD.csv")[["Group State", "Group County", "6p_total"]]
            debt_by_county = debt_by_county.groupby(by="Group County")["6p_total"].sum()
            debt_by_county = debt_by_county.to_frame()
            debt_by_county.reset_index(inplace=True)
            debt_by_county.index.name = "info"
            debt_by_county.rename(columns={"Group County":"county", "Group State":"state"}, inplace=True)


            county_geo_fips = pd.read_csv("../data_raw/census_data/countyPopulation.csv", header=1)[["Geo_FIPS", "Geo_name"]]
            county_geo_fips.rename(columns={"Geo_name":"county"}, inplace=True)
            county_debt_geo = pd.merge(debt_by_county, county_geo_fips, on="county")

            # test debt distribution map 
            # fig = px.choropleth()
            six_p_tot = county_debt_geo["6p_total"]
            x = six_p_tot[six_p_tot.between(six_p_tot.quantile(.15), six_p_tot.quantile(.85))] # remove outliers

            fig = px.choropleth(county_debt_geo, geojson=map_gj, locations='Geo_FIPS', 
                            color='6p_total',
                            color_continuous_scale="Viridis",
                            range_color=(x.min(), 
                                        x.max()),
                            featureidkey="properties.Geo_FIPS",
                            scope="usa",
                            basemap_visible=basemap_visible,
                            fitbounds=fitbounds,
                            hover_name="county",
                            hover_data=["6p_total"]
                        )
            slider =  dcc.RangeSlider(0, 20, value=[5, 15])

        return dcc.Graph(figure = fig, id = "my-map"), slider
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
@app.callback(
        Output('my-map', 'figure'),
        [Input('my-rangeslider', 'value')]
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
