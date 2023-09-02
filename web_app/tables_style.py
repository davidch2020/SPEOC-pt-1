import dash_bootstrap_components as dbc
import pandas as pd

# load the dataset.


df = pd.read_csv('https://raw.githubusercontent.com/liaochris/SPEOC-pt-1/main/data_clean/final_data_CD.csv')
df = df.drop(
    ['Group Match Index', 'Group Match Url', 'Full Search Name', 'assets', 'Name_Fix_Transfer', 'Name_Fix_Clean',
     'imputed_location', 'location conflict', 'Group Village'], axis=1)
df = df.rename(columns={'Unnamed: 0': 'Order', '6p_total': 'Face Value of 6% debt',
                        '6p_def_total': 'Face Value of deferred 6% debt', 'unpaid_interest': 'Unpaid Interest',
                        'final_total': 'Final Total'})
df[['Face Value of 6% debt', 'Face Value of deferred 6% debt', 'Unpaid Interest', '6p_total_adj', '6p_def_total_adj',
    'unpaid_interest_adj', 'Final Total', 'final_total_adj']] = df[
    ['Face Value of 6% debt', 'Face Value of deferred 6% debt', 'Unpaid Interest', '6p_total_adj', '6p_def_total_adj',
     'unpaid_interest_adj', 'Final Total', 'final_total_adj']].round(0)

# Define a CSS stylesheet to enhance the appearance.
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Defining DataTable styling, unpacked later
style_data_table = {
    'maxHeight': '70vh',
    'overflowY': 'scroll',
    'border': 'thin lightgrey solid',
    'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
    'borderRadius': '2px'
}

style_cell = {
    'fontFamily': 'Open Sans',
    'textAlign': 'left',
    'width': '{}%'.format(len(df.columns)),
    'minWidth': '180px',
    'padding': '5px',
    'whiteSpace': 'no-wrap',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'border': '1px solid grey'
}

style_header = {
    'backgroundColor': '#e8f4f2',
    'fontWeight': 'bold',
    'color': '#333333',
    'fontSize': '16px'
}

style_table = {
    'overflowX': 'auto',
}

style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#E8E8E8'
    },
    {
        'if': {'state': 'active'},
        'border': '1px solid #b2deda',
        'color': '#333333'
    }
]

custom_style = {
    'style_table': style_table,
    'style_header': style_header,
    'style_cell': style_cell,
    'style_data_conditional': style_data_conditional
}
