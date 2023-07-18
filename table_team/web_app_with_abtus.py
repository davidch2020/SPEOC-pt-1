import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the navigation bar
navbar = html.Div(
    className='navbar',
    children=[
        html.A('Maps & Tables', href='/maps_tables'),
        html.A('About Us', href='/about_us'),
        html.A('Project Description', href='/project_description')
    ]
)

# Define the layout for Maps & Tables page
maps_tables_layout = html.Div(
    className="page-content",
    children=[
        navbar,
        html.H1("Maps & Tables Page"),
        # Add maps and tables content here
    ],
)

# Define the layout for About Us page
about_us_layout = html.Div(
    className='page',
    children=[
        navbar,
        html.H1('About Us'),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_1', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 1'),
                        html.P('Text description for the first person'),
                        html.A('Link to Personal Website 1', href='link_url_1')
                    ]
                )
            ]
        ),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_2', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 2'),
                        html.P('Text description for the second person'),
                        html.A('Link to Personal Website 2', href='link_url_2')
                    ]
                )
            ]
        ),
        html.Hr(),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_3', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 3'),
                        html.P('Text description for the third person'),
                        html.A('Link to Personal Website 3', href='link_url_3')
                    ]
                )
            ]
        ),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_4', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 4'),
                        html.P('Text description for the fourth person'),
                        html.A('Link to Personal Website 4', href='link_url_4')
                    ]
                )
            ]
        ),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_5', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 5'),
                        html.P('Text description for the fifth person'),
                        html.A('Link to Personal Website 5', href='link_url_5')
                    ]
                )
            ]
        ),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_6', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 6'),
                        html.P('Text description for the sixth person'),
                        html.A('Link to Personal Website 6', href='link_url_6')
                    ]
                )
            ]
        ),
        html.Div(
            className='about-us-section',
            children=[
                html.Img(src='image_url_7', className='headshot'),
                html.Div(
                    className='about-us-description',
                    children=[
                        html.H3('Description 7'),
                        html.P('Text description for the seventh person'),
                        html.A('Link to Personal Website 7', href='link_url_7')
                    ]
                )
            ]
        ),
    ]
)

# Define the layout for Project Description page
project_description_layout = html.Div(
    className="page-content",
    children=[
        navbar,
        html.H1("Project Description Page"),
        # Add project description content here
    ],
)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maps_tables':
        return maps_tables_layout
    elif pathname == '/about_us':
        return about_us_layout
    elif pathname == '/project_description':
        return project_description_layout
    else:
        return maps_tables_layout  # Set the default page to Maps & Tables

# Run the app
if __name__ == '__main__':
    app.run_server(port=8300, debug=True)
