import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='about-section',
            children=[
                html.H1('About Us Page', style={'text-align': 'center'}), #didn't know how to apply this style to all of the code so just spammed it in every line
                html.P(['Insert text about the group.'], style={'text-align': 'center'}),
            ]
        ),
        html.H2('Our Team', style={'text-align': 'center'}),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='column',
                    children=[
                        html.Div(
                            className='card',
                            children=[
                                html.Img(src='[Insert image link here]', alt='Insert image here',
                                         style={'width': '25%', #Think this width has something to do with the images not being centered, dk how to fix
                                                'display': 'block',
                                                'margin-left': 'auto',
                                                'margin-right': 'auto'}),
                                html.Div(
                                    className='container',
                                    children=[
                                        html.H2('[Insert name here]', style={'text-align': 'center'}),
                                        html.P('[Insert role here]', className='title',
                                               style={'text-align': 'center'}),
                                        html.P('[Insert background here]', style={'text-align': 'center'}),
                                        html.P('[Insert email here]', style={'text-align': 'center'}),
                                        html.P(html.Button('Contact', className='button'),
                                               style={'text-align': 'center'})
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            className='column',
                            children=[
                                html.Div(
                                    className='card',
                                    children=[
                                        html.Img(src='[Insert image link here]', alt='Insert image here',
                                                 style={'width': '100%', 'text-align': 'center'}),
                                        html.Div(
                                            className='container',
                                            children=[
                                                html.H2('[Insert name here]', style={'text-align': 'center'}),
                                                html.P('[Insert role here]', className='title',
                                                       style={'text-align': 'center'}),
                                                html.P('[Insert background here]', style={'text-align': 'center'}),
                                                html.P('[Insert email here]', style={'text-align': 'center'}),
                                                html.P(html.Button('Contact', className='button'),
                                                       style={'text-align': 'center'})
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='column',
                                    children=[
                                        html.Div(
                                            className='card',
                                            children=[
                                                html.Img(src='[Insert image link here]', alt='Insert image here',
                                                         style={'width': '100%', 'text-align': 'center'}),
                                                html.Div(
                                                    className='container',
                                                    children=[
                                                        html.H2('[Insert name here]', style={'text-align': 'center'}),
                                                        html.P('[Insert role here]', className='title',
                                                               style={'text-align': 'center'}),
                                                        html.P('[Insert background here]',
                                                               style={'text-align': 'center'}),
                                                        html.P('[Insert email here]', style={'text-align': 'center'}),
                                                        html.P(html.Button('Contact', className='button'),
                                                               style={'text-align': 'center'})
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )



