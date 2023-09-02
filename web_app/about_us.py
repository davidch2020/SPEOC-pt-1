from dash import html
from dash import dcc


def about_us_layout():
    # Headshots and names in different categories
    categories = {
        "Professors": [
            {"name": "Thomas Sargent", "image_url": "image_url_automation_1.jpg", "roles": "PI", "link_url": "https://example.com"},
            {"name": "George Hall", "image_url": "image_url_automation_1.jpg", "roles": "PI", "link_url": "https://example.com"},
        ],
        "Team Members 1": [
            {"name": "Chris Liao", "image_url": "image_url_automation_1.jpg", "roles": "Team Leader", "link_url": "https://www.linkedin.com/in/chris-liao-8865b219a/"},
            {"name": "David Cho", "image_url": "image_url_automation_1.jpg", "roles": "Web App + Data Cleaning", "link_url": "https://example.com"},
            {"name": "Maria Dubasov", "image_url": "image_url_dataviz_2.jpg", "roles": "Web App", "link_url": "https://example.com"}],
        "Team Members 2": [
            {"name": "Peter Gao", "image_url": "image_url_dataviz_2.jpg", "roles": "Web App", "link_url": "https://example.com"},
            {"name": "Jasmine Garcia", "image_url": "image_url_dataviz_2.jpg", "roles": "Web App", "link_url": "https://www.linkedin.com/in/jasminemg/"}],
        "Team Members 3": [
            {"name": "Liam Loughead", "image_url": "image_url_automation_2.jpg", "roles": "Data Cleaning", "link_url": "https://example.com"},
            {"name": "John Mo", "image_url": "image_url_dataviz_2.jpg", "roles": "Web App", "link_url": "https://example.com"}],
    }

    # Helper function to create a single headshot element
    def create_headshot_element(image_url, name, roles, link_url):
        return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        style={
                            "width": "400px",   # Adjust the width as desired
                            "height": "500px",  # Adjust the height as desired
                            "background-color": "#f1f1f1",  # Light grey background color
                            "padding": "20px",  # Add padding
                            "border": "1px solid transparent",  # Thinner border with transparent color
                        },
                        children=[
                            html.Div(
                                style={
                                    "width": "100%",
                                    "height": "70%",
                                    "background-image": f"url('{image_url}')",
                                    "background-size": "cover",
                                    "background-position": "center",
                                    "border-radius": "0%",
                                }
                            ),
                            html.Hr(style={"margin": "20px"}),  # Add horizontal line with margin
                            html.H5(name, className="headshot-name", style={"color": "black"}),
                            html.H5("Roles: " + roles, className="headshot-name", style={"color": "black"}),
                            dcc.Link("Learn more", href=link_url, target="_blank"),
                        ],
                    )
                ],
                style={"text-align": "center", "margin-bottom": "20px"},  # Add margin
                className="headshot-element",
            ),
        ],
        style={
            "display": "inline-block",
            "width": "420px",
            "margin": "0.75in 0",
            "margin-left": "0.5in",
            "position": "relative",
        },
    )

    # Create the layout
    layout = html.Div([
        html.H1("The Team", style={"text-align": "center"}),
        html.Hr(),  # Thin line separating the categories
        
        #Professors Category
        html.H2("Professors", style={"text-align": "center"}),
        html.Div([
            create_headshot_element(person["image_url"], person["name"], person['roles'], person["link_url"])
            for person in categories["Professors"]
        ], style={"display": "flex", "justify-content": "center"}),
        
        html.Hr(style={"height": "2px", "background-color": "black"}),  # Black line separator

        #Team Lead Category
        html.H2("Team Members", style={"text-align": "center"}),
        html.Div([
            create_headshot_element(person["image_url"], person["name"], person['roles'], person["link_url"])
            for person in categories["Team Members 1"]
        ], style={"display": "flex", "justify-content": "center"}),
        
        # Data Automation category
        html.Div([
            create_headshot_element(person["image_url"], person["name"], person['roles'], person["link_url"])
            for person in categories["Team Members 2"]
        ], style={"display": "flex", "justify-content": "center"}),

        # Data Visualization category
        html.Div([
            create_headshot_element(person["image_url"], person["name"], person['roles'], person["link_url"])
            for person in categories["Team Members 3"]
        ], style={"display": "flex", "justify-content": "center"}),

    ], className="about-us-layout")

    return layout