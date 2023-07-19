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
        html.A('Project Description', href='/project_description'),
        html.A('About Us', href='/about_us')
    ],
    style={'text-align': 'right', 'padding': '10px'}
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

# Define the layout for Project Description page
project_description_layout = html.Div(
    className='page',
    children=[
        navbar,
        html.H1('Project Description'),
        html.Div(
            className='project-description',
            children=[
                html.Img(src='image_url_header', className='project-header'),
                html.H3('Times New Roman Font Text', className='project-text')
            ]
        )
    ]
)

# Define the layout for About Us page
about_us_layout = html.Div(
    className='page',
    children=[
        navbar,
        html.H1('About Us'),
        html.Div(
            className='about-section',
            children=[
                html.Div(
                    className='about-person',
                    children=[
                        html.A(
                            html.Img(src='image_url1', className='headshot'),
                            href='https://www.linkedin.com/in/jasminemg/'
                        ),
                        html.H3('Person 1')
                    ]
                ),
                html.Div(
                    className='about-person',
                    children=[
                        html.A(
                            html.Img(src='image_url2', className='headshot'),
                            href='https://www.linkedin.com/in/chris-liao-8865b219a/'
                        ),
                        html.H3('Person 2')
                    ]
                )
            ]
        ),
        html.Hr(),
        html.Div(
            className='about-section',
            children=[
                html.Div(
                    className='about-person-row',
                    children=[
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url3', className='headshot'),
                                    href='link_url3'
                                ),
                                html.H3('Person 3')
                            ]
                        ),
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url4', className='headshot'),
                                    href='link_url4'
                                ),
                                html.H3('Person 4')
                            ]
                        ),
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url5', className='headshot'),
                                    href='link_url5'
                                ),
                                html.H3('Person 5')
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='about-person-row',
                    children=[
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url6', className='headshot'),
                                    href='link_url6'
                                ),
                                html.H3('Person 6')
                            ]
                        ),
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url7', className='headshot'),
                                    href='link_url7'
                                ),
                                html.H3('Person 7')
                            ]
                        ),
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url8', className='headshot'),
                                    href='link_url8'
                                ),
                                html.H3('Person 8')
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='about-person-row',
                    children=[
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url9', className='headshot'),
                                    href='link_url9'
                                ),
                                html.H3('Person 9')
                            ]
                        ),
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url10', className='headshot'),
                                    href='link_url10'
                                ),
                                html.H3('Person 10')
                            ]
                        ),
                        html.Div(
                            className='about-person',
                            children=[
                                html.A(
                                    html.Img(src='image_url11', className='headshot'),
                                    href='link_url11'
                                ),
                                html.H3('Person 11')
                            ]
                        )
                    ]
                )
            ]
        )
    ]
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
