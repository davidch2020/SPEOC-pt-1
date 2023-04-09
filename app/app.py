import pandas as pd
from dash import Dash, html, dcc, dash_table

# Load data
df = pd.read_csv('../S2022/Results/CD_table.csv', index_col=0)[['Search Name', 'Location', '6p_Total']]

# Initialize the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Title section
    html.Div([html.H1('Revolutionary War Debt', style={'text-align': 'center', 'font-weight': 'bold'}),
              html.H4('An Interactive Data App', style={'text-align': 'center'})],
             style={'background-color': '#C2DFFF', 'padding': '20px', 'margin-bottom': '20px'}),
    # Parent div for description and table sections
    html.Div([

        # Description section
        html.Div([html.H3('Description', style={'font-weight': 'bold'}), html.P(
            'This web app displays data related to Revolutionary War debt. You can filter and sort the data using the interactive table below.'), ],
                 style={'width': '30%', 'float': 'left', 'padding': '20px', 'background-color': '#F5F5F5',
                        'margin-top': '20px', 'margin-right': '20px', 'margin-bottom': '0px'}),

        # Table section
        html.Div([dash_table.DataTable(id='table', columns=[{'name': i, 'id': i} for i in df.columns],
                                       data=df.to_dict('records'),
                                       page_current=0,
                                       page_size=10,
                                       style_header={
                                           'backgroundColor': '#C2DFFF',
                                           'fontWeight': 'bold',
                                           'textAlign': 'center'
                                       },
                                       sort_mode='multi',
                                       filter_action="native",
                                       sort_action="native",
                                       style_data_conditional=[
                                           {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
                                       style_cell={'textAlign': 'right',
                                                   'whiteSpace': 'normal',
                                                   'overflow': 'hidden',
                                                   'textOverflow': 'ellipsis',
                                                   },
                                       fill_width=False)
                  ], style={'width': '70%', 'float': 'right', 'position': 'relative','padding': '20px', 'background-color': '#F5F5F5',
                            'margin-top': '20px', 'margin-right': '20px', 'margin-bottom': '0px'}),
    ], style={'display': 'flex', 'align-items': 'flex-start'})
])

# Run the app
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8080, debug=True)
