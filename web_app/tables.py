# import packages
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html

# import info from other pages
from app import app
from tables_style import custom_style, df

########################################################################################################################
######################################### Define App Components ########################################################
########################################################################################################################
# Project description tab
table_desc = html.Div(className='box', children=[
    html.H2(children='Table Guide', className='box-title', style={'marginBottom': '20px'}),
    dcc.Markdown('''
        This is a table, aggregated at the debtholder level, of debt certificates redeemed after Hamilton's Plan. 
        - To analyze the data at an aggretate level, click the **Analyze Data** button below. 
        - To analyze the data at the debt holder level, the table allows you to select which columns to display and sort and filter based on row values. 
        
        ##### Table Capabilities
        - **Toggle Columns** allows you to select which columns are included in the table. 
        - To sort the data, click on the arrow pointing upwards to sort in ascending order, or downwards to sort in descending order. 
        - There are four ways to filter the data, 2 for categorical and 2 for numerical data

        ** Categorical Methods**

        1. **Contains:** This can be used with string columns to filter rows that contain a specific substring. For example, typing `NY` will show rows where the column contains the substring 'NY'.
        2. **Multiple values:** If you want to filter rows that match any of several values, you can provide the values separated by commas. For example, typing `"NY", "CT"` will show rows where 'Group State' is either 'NY' or 'CT'.
        
        **Numerical Methods**

        3. **Greater than (>), less than (<), greater than or equal to (>=), less than or equal to (<=):** These can be used with numeric columns to filter rows based on greater than, less than, or equal conditions. For example, in a numeric column like 'Face Value of 6% debt', typing `>500` will show rows where 'Face Value of 6% debt' is greater than 500.
        4. **Ranges for numeric columns:** If you want to filter a numeric column for a range of values, you can provide the range in the format `low-high`. For example, typing `1000-2000` in a numeric column's filter box will show rows where the column value is between 1000 and 2000.

        Note: The filter query is case-sensitive, so make sure to use the correct case when typing your filter queries. 
    ''',
                 id='guide',
                 style={"display": "none"},  # Initially hide the guide
                 ),
    html.Button("Show Guide", id="toggle-button", n_clicks=1),
])

dash_table = html.Div(dash_table.DataTable(
    id='DataTable',
    data=df.to_dict('records'),  # convert the pd dataframe into a dictionary, otherwise Dash cannot process it.
    # make columns toggleable
    columns=[{"name": i, "id": i, 'hideable': True} for i in df.columns],
    # first two arguments of dash_table.DataTable are data & columns by default.
    hidden_columns=["6p_total_adj", "6p_def_total_adj", "unpaid_interest_adj", "final_total_adj"],
    # Unpacking the style dictionary
    **custom_style,
    # Set Interactivity rules:
    editable=True,
    filter_action="custom",
    sort_action="native",
    sort_mode="multi",
    selected_columns=[],
    selected_rows=[],
    page_size=10,
    css=[
        {'selector': '.dash-spreadsheet-menu', 'rule': 'position:absolute;bottom:-5px'},  # move below table
    ]))
# Bottom Display tab with DataFrame/Map
display_tab = html.Div(className='box', children=[
    html.H3(children='Table', className='box-title', style={'textAlign': 'center'}),
    dash_table
], style={'width': '100%', 'overflow': 'auto'})

# Button to open the modal
display_more = dbc.Button("Analyze Data", id="open-button", style={ 'width':'100%'})
display_more_tab = html.Div(className='box', children=[
    display_more
], style={'width': '100%', 'overflow': 'auto', 'posotion': 'relative'})

grouped_charts = html.Div(dbc.Modal([
    dbc.ModalHeader("Chart and Data Options"),
    dbc.ModalBody([
        dcc.Dropdown(id='dropdown', options=[
            {'label': 'Group by State', 'value': 'state'},
            {'label': 'Group by County', 'value': 'county'},
            {'label': 'Group by Town', 'value': 'town'},
            {'label': 'Group by Occupation', 'value': 'occupation'}],
                     value='state'),
        dcc.Dropdown(id='aggregation-dropdown', options=[
            {'label': 'Sum', 'value': 'sum'},
            {'label': 'Average', 'value': 'mean'},
            {'label': 'Min', 'value': 'min'},
            {'label': 'Max', 'value': 'max'}],
                     value='sum'),
        dcc.Dropdown(id='chart-type-dropdown', options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'}],
                     value='bar'),
        html.Div([
            dcc.Checklist(options=[{'label': 'Show "not listed" values', 'value': 'SHOW_NOT_LISTED'}],
                          value=[], id='show-not-listed-checkbox')]),
        html.Br(),
        html.Div(id='derived-table-container', style={"display": "none"},  # Initially hide the table
                 ),
        html.Label("Please select the number of records you want to display:"),
        html.Div(
            id='state-slider-container',
            children=[dcc.Slider(id='state-slider', min=10, max=df['Group State'].nunique(), step=1, value=10,
                                 marks={10: '10', df['Group State'].nunique(): str(df['Group State'].nunique())})]),
        html.Div(id='county-slider-container',
                 children=[dcc.Slider(id='county-slider', min=10, max=df['Group County'].nunique(), step=1, value=10,
                                      marks={10: '10',
                                             df['Group County'].nunique(): str(df['Group County'].nunique())})]),
        html.Div(id='town-slider-container',
                 children=[dcc.Slider(id='town-slider', min=10, max=df['Group Town'].nunique(), step=1, value=10,
                                      marks={10: '10', df['Group Town'].nunique(): str(df['Group Town'].nunique())})]),
        html.Div(id='occupation-slider-container',
                 children=[dcc.Slider(id='occupation-slider', min=10, max=df['occupation'].nunique(), step=1, value=10,
                                      marks={10: '10', df['occupation'].nunique(): str(df['occupation'].nunique())},)]),
        html.Div(id='DataTable Container'),
        html.Div(id="chart-container")], style={ 'overflow': 'auto'}),
    dbc.ModalFooter(dbc.Button("Close", id="close-button", className="ml-auto"))
], id="modal", size='xl'))
tables_layout = [table_desc, display_more_tab, display_tab, grouped_charts]


@app.callback(
    [Output('derived-table-container', 'style'), Output('chart-container', 'children')],
    [Input('DataTable', "derived_virtual_data"),
     Input('DataTable', "derived_virtual_selected_rows"),
     Input('dropdown', "value"),
     Input('aggregation-dropdown', "value"),
     Input('chart-type-dropdown', "value"),
     Input('state-slider', 'value'),
     Input('county-slider', 'value'),
     Input('town-slider', 'value'),
     Input('occupation-slider', 'value'),
     Input('show-not-listed-checkbox', 'value')]
)
def update_graphs(rows, derived_virtual_selected_rows, dropdown_value, aggregation_method, chart_type, state_n,
                  county_n, town_n, occupation_n, checkbox_values):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)
    dff_chart = dff.fillna("not listed")  # Copy of DataFrame for the charts

    show_not_listed = 'SHOW_NOT_LISTED' in checkbox_values
    if not show_not_listed:
        if dropdown_value in ['state', 'county', 'town']:
            dff_chart = dff_chart[dff_chart['Group ' + dropdown_value.capitalize()] != 'not listed']
        elif dropdown_value == 'occupation':
            dff_chart = dff_chart[dff_chart['occupation'] != 'not listed']

    # Data Preprocessing
    # aggregate data
    agg_columns = ["Face Value of 6% debt", "Face Value of deferred 6% debt", "Unpaid Interest", "Final Total"]
    dff_group_state = dff_chart.groupby("Group State")[agg_columns].sum().reset_index()
    df_occupation = dff_chart.copy()  # Use dff_chart here
    # Split "Occupation" column on "|" and explode it into multiple rows
    df_occupation['occupation'] = df_occupation['occupation'].str.split('|')
    df_occupation = df_occupation.explode('occupation')
    df_occupation['occupation'] = df_occupation['occupation'].str.strip()  # remove leading and trailing spaces
    dff_occupation = df_occupation.groupby("occupation")[agg_columns].sum().reset_index()

    # options to choose aggregation method
    if aggregation_method == 'sum':
        dff_group_state = dff_chart.groupby("Group State")[agg_columns].sum().reset_index()
        dff_occupation = df_occupation.groupby("occupation")[agg_columns].sum().reset_index()
    elif aggregation_method == 'mean':
        dff_group_state = dff_chart.groupby("Group State")[agg_columns].mean().reset_index()
        dff_occupation = df_occupation.groupby("occupation")[agg_columns].mean().reset_index()
    elif aggregation_method == 'min':
        dff_group_state = dff_chart.groupby("Group State")[agg_columns].min().reset_index()
        dff_occupation = df_occupation.groupby("occupation")[agg_columns].min().reset_index()
    elif aggregation_method == 'max':
        dff_group_state = dff_chart.groupby("Group State")[agg_columns].max().reset_index()
        dff_occupation = df_occupation.groupby("occupation")[agg_columns].max().reset_index()

    dff_group_county = dff_chart.groupby("Group County")[agg_columns].sum().reset_index()
    dff_group_town = dff_chart.groupby("Group Town")[agg_columns].sum().reset_index()

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9' for i in range(len(dff))]

    charts = []  # Initialize charts as an empty list

    # state
    if dropdown_value == 'state':
        if chart_type in ['bar', 'pie']:
            charts = generateGraph(dff_group_state, 'Group State', chart_type, state_n, colors, dff)
    # county
    elif dropdown_value == 'county':
        # Code for county grouping
        if chart_type in ['bar', 'pie']:
            charts = generateGraph(dff_group_county, 'Group County', chart_type, state_n, colors, dff)
    # town
    elif dropdown_value == 'town':
        # Code for county grouping
        if chart_type in ['bar', 'pie']:
            charts = generateGraph(dff_group_town, 'Group Town', chart_type, state_n, colors, dff)
    # occupation
    elif dropdown_value == 'occupation':
        # Code for county grouping
        if chart_type in ['bar', 'pie']:
            charts = generateGraph(dff_occupation, dropdown_value, chart_type, state_n, colors, dff)

    # Check if charts should be displayed
    if dropdown_value is not None and aggregation_method is not None:
        style = {'display': 'block', 'overflow':'auto'}
    else:
        style = {'display': 'none'}

    return style, charts


@app.callback(
    Output('derived-table-container', "children"),
    [Input('dropdown', "value"),
     Input('aggregation-dropdown', "value"),
     Input('show-not-listed-checkbox', 'value')]
)
def update_derived_table(dropdown_value, aggregation_method, show_not_listed_values):
    dff = df.copy()
    dff_chart = dff.fillna("not listed")  # Copy of DataFrame for the charts


    if not show_not_listed_values:
        if dropdown_value in ['state', 'county', 'town']:
            dff_chart = dff_chart[dff_chart['Group ' + dropdown_value.capitalize()] != 'not listed']
        elif dropdown_value == 'occupation':
            dff_chart = dff_chart[dff_chart['occupation'] != 'not listed']

    agg_columns = ["Face Value of 6% debt", "Face Value of deferred 6% debt", "Unpaid Interest", "Final Total"]

    if dropdown_value == 'state':
        dff_grouped = dff_chart.groupby("Group State")[agg_columns].agg(aggregation_method).reset_index()
        dff_grouped = dff_grouped.sort_values(by="Face Value of 6% debt", ascending=False)
    elif dropdown_value == 'occupation':
        df_occupation = dff_chart.copy()
        df_occupation['occupation'] = df_occupation['occupation'].str.split('|')
        df_occupation = df_occupation.explode('occupation')
        df_occupation['occupation'] = df_occupation['occupation'].str.strip()
        dff_grouped = df_occupation.groupby("occupation")[agg_columns].agg(aggregation_method).reset_index()
        dff_grouped = dff_grouped.sort_values(by="Face Value of 6% debt", ascending=False)
    elif dropdown_value == 'county':
        dff_grouped = dff_chart.groupby("Group County")[agg_columns].agg(aggregation_method).reset_index()
        dff_grouped = dff_grouped.sort_values(by="Face Value of 6% debt", ascending=False)
    elif dropdown_value == 'town':
        dff_grouped = dff_chart.groupby("Group Town")[agg_columns].agg(aggregation_method).reset_index()
        dff_grouped = dff_grouped.sort_values(by="Face Value of 6% debt", ascending=False)

    for col in agg_columns:
        dff_grouped[col] = dff_grouped[col].round(0)
    if type(dash_table) != html.Div:
        return dash_table.DataTable(
            data=dff_grouped.to_dict('records'),
            columns=[{"name": i, "id": i} for i in dff_grouped.columns],
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'grey',
                'fontWeight': 'bold'
            },
            style_data={
                'backgroundColor': 'white',
                'color': 'black'
            },
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
        )


@app.callback(
    [Output('state-slider-container', 'style'),
     Output('occupation-slider-container', 'style'),
     Output('county-slider-container', 'style'),
     Output('town-slider-container', 'style')],
    [Input('dropdown', 'value')]
)
def toggle_slider(dropdown_value):
    if dropdown_value == 'state':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    elif dropdown_value == 'occupation':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    elif dropdown_value == 'county':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    elif dropdown_value == 'town':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}


@app.callback(
    Output("guide", "style"),
    Output("toggle-button", "children"),
    [Input("toggle-button", "n_clicks")]
)
def toggle_guide(n):
    if n % 2 == 0:
        # If the button has been clicked an even number of times, hide the guide
        return {"display": "none"}, "Show Guide"
    else:
        # If the button has been clicked an odd number of times, show the guide
        return {"display": "block"}, "Hide Guide"


@app.callback(
    Output("modal", "is_open"),
    [Input("open-button", "n_clicks"), Input("close-button", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open


# Define the callback to update the table
@app.callback(
    Output('DataTable', 'data'),
    [Input('DataTable', 'filter_query')]
)
def update_table(filter_query):
    if filter_query is None:
        # No filters applied
        return df.to_dict('records')

    df_filtered = df.copy()
    filtering_expressions = filter_query.split(' && ')
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if filter_value is None:
            continue

        if df[col_name].dtype != 'object':  # If it's a numeric column
            if '-' in str(filter_value):
                low, high = [float(v) for v in filter_value.split('-')]
                df_filtered = df_filtered.loc[(df_filtered[col_name] >= low) & (df_filtered[col_name] <= high)]
            elif operator in ('gt'):
                df_filtered = df_filtered.loc[df_filtered[col_name] > filter_value]
            elif operator in ('lt'):
                df_filtered = df_filtered.loc[df_filtered[col_name] < filter_value]
            elif operator in ('ge'):
                df_filtered = df_filtered.loc[df_filtered[col_name] >= filter_value]
            elif operator in ('le'):
                df_filtered = df_filtered.loc[df_filtered[col_name] <= filter_value]
            elif operator in ('ne'):
                df_filtered = df_filtered.loc[df_filtered[col_name] != filter_value]
            elif operator in ('eq'):
                df_filtered = df_filtered.loc[df_filtered[col_name] == filter_value]
            else:
                df_filtered = df_filtered.loc[df_filtered[col_name] == float(filter_value)]
        else:  # If it's a string column
            df_filtered = df_filtered.dropna(subset=[col_name])
            if ',' in str(filter_value):
                # Multiple values provided
                # values = str(filter_value).split(',')
                values = [v.strip() for v in str(filter_value).split(',')]
                df_filtered = df_filtered[df_filtered[col_name].isin(values)]
            elif operator == 'contains':
                df_filtered = df_filtered.loc[df_filtered[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # This is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                df_filtered = df_filtered.loc[df_filtered[col_name].str.startswith(filter_value)]
    return df_filtered.to_dict('records')


# This function parses the filter string into column name, operator and filter value
def split_filter_part(filter_part):
    for operator_type, operator_string in [('eq', '=='),
                                           ('ne', '!='),
                                           ('lt', '< '),
                                           ('le', '<= '),
                                           ('gt', '> '),
                                           ('ge', '>= '),
                                           ('contains', 'contains '),
                                           ('datestartswith', 'datestartswith ')]:
        if operator_string in filter_part:
            name_part, value_part = filter_part.split(operator_string, 1)
            name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
            value_part = value_part.strip()
            v0 = value_part[0]
            if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                value = value_part[1: -1].replace('\\' + v0, v0)
            else:
                try:
                    value = float(value_part)
                except ValueError:
                    value = value_part
            return name, operator_type, value

    return [None] * 3



def generateGraph(df, col, type, max_count, colors, dff):
    if type == 'pie':
        charts = [dcc.Graph(
            id=column if type != 'occupation' else column + '-occupation',
            figure={"data": [{"labels": df.sort_values(by=column, ascending=False)[col].head(max_count),
                              "values": df.sort_values(by=column, ascending=False)[column].head(max_count),
                              "type": type}],
                    "layout": {"title": {"text": column},
                               "height": '10vh',
                               "margin": { "l": 10, "r": 10},},},)
            for column in
            ["Face Value of 6% debt", "Face Value of deferred 6% debt", "Unpaid Interest", "Final Total"] if
            column in dff]
    elif type == 'bar':
        charts = [dcc.Graph(
            id=column if type != 'occupation' else column + '-occupation',
            figure={"data": [{"x": df.sort_values(by=column, ascending=False)[col].head(max_count),
                              "y": df.sort_values(by=column, ascending=False)[column].head(max_count),
                              "type": type,
                              "marker": {"color": colors}, }],
                    "layout": {"xaxis": {"automargin": True},
                               "yaxis": {
                                   "automargin": True,
                                   "title": {"text": column}},
                               "height": 250,
                               "margin": {"t": 10, "l": 10, "r": 10},},},)
            for column in
            ["Face Value of 6% debt", "Face Value of deferred 6% debt", "Unpaid Interest", "Final Total"] if
            column in dff]
    return charts
