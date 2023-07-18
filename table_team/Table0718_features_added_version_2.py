#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
from dash import dash_table
import pandas as pd
from dash import dcc
from dash import html
from dash import Input, Output, callback, State
import dash_bootstrap_components as dbc



# load the dataset.

url = 'https://raw.githubusercontent.com/liaochris/SPEOC-pt-1/main/data_clean/final_data_CD.csv'

df = pd.read_csv(url) 
df = df.drop(['Group Match Index', 'Group Match Url', 'Full Search Name', 'assets', 'Name_Fix_Transfer', 'Name_Fix_Clean', 'imputed_location', 'location conflict', 'Group Village'], axis=1)
df = df.rename(columns={'Unnamed: 0': 'Order', '6p_total': 'Face Value of 6% debt', '6p_def_total': 'Face Value of deferred 6% debt', 'unpaid_interest': 'Unpaid Interest', 'final_total': 'Final Total'})
df[['Face Value of 6% debt', 'Face Value of deferred 6% debt', 'Unpaid Interest', '6p_total_adj', '6p_def_total_adj', 'unpaid_interest_adj', 'Final Total', 'final_total_adj']] = df[['Face Value of 6% debt', 'Face Value of deferred 6% debt', 'Unpaid Interest', '6p_total_adj', '6p_def_total_adj', 'unpaid_interest_adj', 'Final Total', 'final_total_adj']].round(0)


# Initialize the app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("DataTable of Creditors", style={'text-align': 'center'}), # name the Main Headline H1

    html.Button("Toggle Guide", id="toggle-button", n_clicks=0),
    
    dcc.Markdown('''
        ## Guide to Filtering in the DataTable

        The Dash DataTable provides a built-in, interactive filter that users can use to filter data in real-time. Here's how you can use it:

        1. **Contains:** This can be used with string columns to filter rows that contain a specific substring. For example, typing `NY` will show rows where the column contains the substring 'NY'.
        2. **Greater than (>), less than (<), greater than or equal to (>=), less than or equal to (<=):** These can be used with numeric columns to filter rows based on greater than, less than, or equal conditions. For example, in a numeric column like 'Face Value of 6% debt', typing `>500` will show rows where 'Face Value of 6% debt' is greater than 500.
        3. **Multiple values:** If you want to filter rows that match any of several values, you can provide the values separated by commas. For example, typing `"NY", "CT"` will show rows where 'Group State' is either 'NY' or 'CT'.
        4. **Ranges for numeric columns:** If you want to filter a numeric column for a range of values, you can provide the range in the format `low-high`. For example, typing `1000-2000` in a numeric column's filter box will show rows where the column value is between 1000 and 2000.

        Note: The filter query is case-sensitive, so make sure to use the correct case when typing your filter queries. 
    ''',
        id = 'guide',
        style={"display": "none"},  # Initially hide the guide
    ),

    dash_table.DataTable(
        id = 'DataTable',
        data=df.to_dict('records'),  # convert the pd dataframe into a dictionary, otherwise Dash cannot process it.
        # make columns toggleable 
        columns=[{"name": i, "id": i, 'hideable': True} for i in df.columns],
        # first two arguments of dash_table.DataTable are data & columns by default.
        
        style_cell={'textAlign': 'left'}, # align the texts in columns to the left
        style_cell_conditional=[
        {
            'if': {'column_id': 'Region'},
            'textAlign': 'left'
        }
    ],
        
      
        style_header={
        'backgroundColor': 'lightblue',
        'fontWeight': 'bold',
        'font-family': 'Helvetica'
    }, # To style the header, I changed the color of our header (random color) and make the font bold.
        
        style_data={
        'backgroundColor': 'white',
        'color': 'black'
    }, # I can also change the color of data.


        
# Interactivity starts here:
        editable=True,
        filter_action="custom",
        sort_action="native",
        sort_mode="multi",

        selected_columns=[],
        selected_rows=[],
        page_size= 10,

        
    ),
    
    # Button to open the modal
    dbc.Button("Open chart options", id="open-button"),
    
    dbc.Modal([
        dbc.ModalHeader("Chart Options"),
        dbc.ModalBody([
    
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Group by State', 'value': 'state'},
                    {'label': 'Group by Occupation', 'value': 'occupation'}
                ],
                value='state'
            ),

            dcc.Dropdown(
                id='aggregation-dropdown',
                options=[
                    {'label': 'Sum', 'value': 'sum'},
                    {'label': 'Average', 'value': 'mean'},
                    {'label': 'Min', 'value': 'min'},
                    {'label': 'Max', 'value': 'max'}
                ],
                value='sum'
            ),

            html.Br(),
            html.Label("Please select the number of records you want to display:"),
            html.Div(
                id='state-slider-container',
                children=[
                    dcc.Slider(
                        id='state-slider',
                        min=10,
                        max=df['Group State'].nunique(),
                        step=1,
                        value=10,
                        marks={10: '10', df['Group State'].nunique(): str(df['Group State'].nunique())},
                        style={'color': 'red', 'background-color': 'lightyellow'}
                    )
                ]
            ),


            html.Div(
                id='occupation-slider-container',
                children=[
                    dcc.Slider(
                        id='occupation-slider',
                        min=10,
                        max=df['occupation'].nunique(),
                        step=1,
                        value=10,
                        marks={10: '10', df['occupation'].nunique(): str(df['occupation'].nunique())},
                        style={'color': 'green', 'background-color': 'lightblue'}
                    )
                ]
            ),
            html.Div(id = 'DataTable Container')

        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-button", className="ml-auto")
        )
    ], id="modal"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Bar Chart 1", style={'font-family': 'Arial', 'color': 'purple'}),
                dbc.CardBody([
                    dcc.Graph(id='bar-chart-1')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Bar Chart 2", style={'font-family': 'Arial', 'color': 'orange'}),
                dbc.CardBody([
                    dcc.Graph(id='bar-chart-2')
                ])
            ])
        ], width=6)
    ])
    
])


@callback(
    Output('DataTable Container', "children"),
    [Input('DataTable', "derived_virtual_data"),
    Input('DataTable', "derived_virtual_selected_rows"),
    Input('dropdown', "value"),
    Input('aggregation-dropdown', "value"),
    Input('state-slider', 'value'),
    Input('occupation-slider', 'value')])

def update_graphs(rows, derived_virtual_selected_rows, dropdown_value, aggregation_method, state_n, occupation_n):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)
    dff_chart = dff.fillna("not listed")  # Copy of DataFrame for the charts

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
        
    
    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]
    if dropdown_value=='state':
        charts = [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff_group_state.sort_values(by=column, ascending=False)["Group State"].head(state_n),
                            "y": dff_group_state.sort_values(by=column, ascending=False)[column].head(state_n),
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": column}
                        },
                        "height": 130,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )
            for column in ["Face Value of 6% debt", "Face Value of deferred 6% debt", "Unpaid Interest", "Final Total"] if column in dff
        ]
    else: 
        
        charts = [
            dcc.Graph(
                id=column+'-occupation',
                figure={
                    "data": [
                        {

                            "x": dff_occupation.sort_values(by=column, ascending=False)["occupation"].head(occupation_n),
                            "y": dff_occupation.sort_values(by=column, ascending=False)[column].head(occupation_n),
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": column}
                        },
                        "height": 130,
                        "margin": {"t": 10, "l": 10, "r": 10},
                        "font":{'family': 'Helvetica', color: 'darkblue'},
                        "plot_bgcolor": 'lightgray', 
                        "paper_bgcolor": 'whitesmoke',
                    },
                },
            )
            for column in ["Face Value of 6% debt", "Face Value of deferred 6% debt", "Unpaid Interest", "Final Total"] if column in dff
        ]
        
        

    return charts

@app.callback(
    [Output('state-slider-container', 'style'),
     Output('occupation-slider-container', 'style')],
    [Input('dropdown', 'value')]
)
def toggle_slider(dropdown_value):
    if dropdown_value == 'state':
        return {'display': 'block'}, {'display': 'none'}
    elif dropdown_value == 'occupation':
        return {'display': 'none'}, {'display': 'block'}


@app.callback(
    Output("guide", "style"),
    [Input("toggle-button", "n_clicks")]
)
def toggle_guide(n):
    if n % 2 == 0:
        # If the button has been clicked an even number of times, hide the guide
        return {"display": "none"}
    else:
        # If the button has been clicked an odd number of times, show the guide
        return {"display": "block"}

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
                #values = str(filter_value).split(',')
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

        

if __name__ == '__main__':
    app.run_server(debug=True, port=8089)


# In[ ]:




