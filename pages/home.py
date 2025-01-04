import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Initialize the Dash app
dash.register_page(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],path='/')

# Define the layout
layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f8f9fa", "margin": "0", "padding": "0"},
    children=[
        # Navigation Bar
        html.Div(
    style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "padding": "0px 50px",
        "backgroundColor": "#6a0dad",
        "color": "white",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "position": "fixed",  # Makes the navbar fixed at the top
        "top": 0,
        "left":0,   
        "width": "95%",
        "zIndex": 1000  
    },
    children=[
        # Logo Section
        html.Div(
            children=[
                html.Img(
                    src="/assets/logo.png",  
                    style={
                        "height": "60px",
                        "marginRight": "20px",
                    }
                ),
                html.Div("ExcelXpert", style={"fontSize": "24px", "fontWeight": "bold"}),
            ],
            style={"display": "flex", "alignItems": "center"}
        ),
        
        # Links Section
        html.Div(
            children=[
                html.A(
                    "Home", href="#", 
                    style={
                        "color": "white", 
                        "marginRight": "20px", 
                        "textDecoration": "none", 
                        "fontWeight": "bold", 
                        "fontSize": "18px",
                    },
                    className="nav-link"
                ),
                html.A(
                    "About", href="#about", 
                    style={
                        "color": "white", 
                        "marginRight": "20px", 
                        "textDecoration": "none", 
                        "fontWeight": "bold", 
                        "fontSize": "18px",
                    },
                    className="nav-link"
                ),
                html.A(
                    "Services", href="#services", 
                    style={
                        "color": "white", 
                        "marginRight": "20px", 
                        "textDecoration": "none", 
                        "fontWeight": "bold", 
                        "fontSize": "18px",
                    },
                    className="nav-link"
                ),
                html.A(
                    "Portfolio", href="#portfolio", 
                    style={
                        "color": "white", 
                        "marginRight": "20px", 
                        "textDecoration": "none", 
                        "fontWeight": "bold", 
                        "fontSize": "18px",
                    },
                    className="nav-link"
                ),
                html.A(
                    "Team", href="#team", 
                    style={
                        "color": "white", 
                        "marginRight": "20px", 
                        "textDecoration": "none", 
                        "fontWeight": "bold", 
                        "fontSize": "18px",
                    },
                    className="nav-link"
                ),
                html.A(
                    "Contact", href="#contact", 
                    style={
                        "color": "white", 
                        "textDecoration": "none", 
                        "fontWeight": "bold", 
                        "fontSize": "18px",
                    },
                    className="nav-link"
                ),
            ],
            style={"display": "flex", "alignItems": "center"}
        ),
    ],
),


        # Hero Section
        html.Div(
            style={
                "textAlign": "center",
                "padding": "100px 20px",
                "background": "linear-gradient(135deg, #a155b9, #6a0dad)",
                "color": "white",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
            },
            children=[
                html.H1("Welcome to ExcelXpert App", style={"fontSize": "48px", "marginBottom": "28px", "fontWeight": "bold", "marginTop": "50px"}),
                html.P("Transforming Your Data Into Stunning Visualizations: 2D & 3D Insights Made Effortless", style={"fontSize": "28px", "fontWeight": "bold"}),
                html.P("Discover the power of dynamic data visualization with our app. Whether it's 2D graphs or immersive 3D models, we empower you to interpret your Excel data like never before.", style={"fontSize": "20px"}),
                html.P("Upload, customize, and explore your insights are just a click away.", style={"fontSize": "20px"}),
                dcc.Link('Get Started', href='/login',style={
                    "padding": "10px 20px",
                    "fontSize": "18px",
                    "backgroundColor": "white",
                    "color": "#6a0dad",
                    "border": "none",
                    "cursor": "pointer",
                    "borderRadius": "5px", "fontWeight": "bold",
                    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
                })
            ],
        ),

        # About Section
        html.Div(
            id="about",
            style={"padding": "50px", "backgroundColor": "#f2f2f2"},
            children=[
                html.H2("About Us", style={"textAlign": "center", "marginBottom": "40px", "color": "#6a0dad", "fontWeight": "bold"}),
                html.P(
                    "At ExcelXpert, we are passionate about turning raw data into meaningful stories. Our platform provides an innovative way to visualize Excel data dynamically, helping you analyze and present complex information with ease. From researchers to analysts, anyone can leverage our user-friendly interface to gain deeper insights. Join us in revolutionizing the way data is understood and communicated. "
                    ,
                    style={"textAlign": "center", "fontSize": "20px", "maxWidth": "1000px", "margin": "0 auto"}
                ),
            ],
        ),

        # Services Section
        html.Div(
            id="services",
            style={"padding": "50px", "backgroundColor": "white"},
            children=[
                html.H2("Our Services", style={"textAlign": "center", "marginBottom": "40px", "color": "#6a0dad", "fontWeight": "bold"}),
                dbc.Row(
                    children=[
                        dbc.Col(
                            html.Div(
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#f8f9fa",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                    html.H4("Dynamic 2D Visualization", style={"color": "#6a0dad"}),
                                    html.P("Transform complex data into crisp, interactive 2D graphs, including bar charts, line graphs, scatter plots, and more. "
                                           "Customize colors, labels, and layouts to match your presentation style. "
                                           "Perfect for reports, academic projects, and quick data analysis."
                                           ),
                                ],
                            ), width=4
                        ),
                        dbc.Col(
                            html.Div(
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#f8f9fa",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                    html.H4("Immersive 3D Visualization", style={"color": "#6a0dad"}),
                                    html.P("Step beyond static visuals with 3D surface plots, wireframes, and volumetric data renderings. "
                                           "Rotate, zoom, and explore data in an interactive 3D space to uncover hidden patterns. "
                                           "Ideal for geospatial data, engineering designs, and advanced analytics. "),
                                ],
                            ), width=4
                        ),
                        dbc.Col(
                            html.Div(
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#f8f9fa",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                    html.H4("Intuitive Parameter Adjustment", style={"color": "#6a0dad"}),
                                    html.P("Modify parameters like axis ranges, grid density, and labels in real-time. "
                                           "Use sliders, dropdowns, and other user-friendly controls to refine your visualizations. "
                                           "Empower users of all technical levels to create polished outputs without coding knowledge. "
                                           ),
                                ],
                            ), width=4
                        ),
                    ]
                ),
            ],
        ),

       # Portfolio Section
html.Div(
    id="portfolio",
    style={"padding": "50px", "backgroundColor": "#f2f2f2"},
    children=[
        html.H2("Portfolio", style={"textAlign": "center", "marginBottom": "40px", "color": "#6a0dad", "fontWeight": "bold"}),
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(
                        style={
                            "padding": "20px",
                            "backgroundColor": "white",
                            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                            "borderRadius": "10px"
                        },
                        children=[
                            html.Img(src="/assets/heatmap_plasma.png", style={"width": "90%", "borderRadius": "10px", "marginBottom": "20px"}),  # Add the image here
                            html.H4("3D Surface Modeling", style={"color": "#6a0dad"}),
                            html.P("Explore how our app visualizes geospatial data in 3D, providing unparalleled clarity."),
                        ],
                    ), width=4
                ),
                dbc.Col(
                    html.Div(
                        style={
                            "padding": "20px",
                            "backgroundColor": "white",
                            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                            "borderRadius": "10px"
                        },
                        children=[
                            html.Img(src="/assets/3d_cylinder_plasma.png", style={"width": "100%", "heigh": "100%", "borderRadius": "10px", "marginBottom": "20px"}),  # Add the image here
                            html.H4("Custom Solutions for Industries", style={"color": "#6a0dad"}),
                            html.P("Tailored visualizations for healthcare, finance, manufacturing, Retail & E-commerce, and more."),
                        ],
                    ), width=4
                ),
                dbc.Col(
                    html.Div(
                        style={
                            "padding": "20px",
                            "backgroundColor": "white",
                            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                            "borderRadius": "10px"
                        },
                        children=[
                            html.Img(src="/assets/3d_surface_plasma.png", style={"width": "93%", "borderRadius": "10px", "marginBottom": "20px"}),  # Add the image here
                            html.H4("Product Design Data Analysis", style={"color": "#6a0dad"}),
                            html.P("Witness the transformation of engineering specifications into interactive graphs. "),
                        ],
                    ), width=4
                ),
            ]
        ),
    ],
),


        # Team Section
        html.Div(
            id="team",
            style={"padding": "50px", "backgroundColor": "#f2f2f2"},
            children=[
                html.H2("Meet the Team", style={"textAlign": "center", "marginBottom": "40px", "color": "#6a0dad", "fontWeight": "bold"}),
                dbc.Row(
                    children=[
                        dbc.Col(
                            html.Div(
                                style={
                                    "textAlign": "center",
                                    "padding": "20px",
                                    "backgroundColor": "white",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                    html.Img(src="/assets/team1.jpg", style={"width": "200px", 
        "height": "200px", 
        "borderRadius": "50%", 
        "objectFit": "cover"}),
                                    html.H4("Bhavesh Sonar", style={"color": "#6a0dad", "marginTop": "10px"}),
                                    html.P("CEO & Founder"),
                                ],
                            ), width=3
                        ),
                        dbc.Col(
                            html.Div(
                                style={
                                    "textAlign": "center",
                                    "padding": "20px",
                                    "backgroundColor": "white",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                   html.Img(src="/assets/team2.jpg", style={"width": "200px", 
        "height": "200px", 
        "borderRadius": "50%", 
        "objectFit": "cover"}),

                                    html.H4("Tejashree Mulinti", style={"color": "#6a0dad", "marginTop": "10px"}),
                                    html.P("Lead Designer"),
                                ],
                            ), width=3
                        ),
                        dbc.Col(
                            html.Div(
                                style={
                                    "textAlign": "center",
                                    "padding": "20px",
                                    "backgroundColor": "white",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                    html.Img(src="/assets/team3.jpg", style={"width": "200px", 
        "height": "200px", 
        "borderRadius": "50%", 
        "objectFit": "cover"}),
                                    html.H4("Siddhi Adhav", style={"color": "#6a0dad", "marginTop": "10px"}),
                                    html.P("Developer"),
                                ],
                            ), width=3
                        ),
                        dbc.Col(
                            html.Div(
                                style={
                                    "textAlign": "center",
                                    "padding": "20px",
                                    "backgroundColor": "white",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                    "borderRadius": "10px"
                                },
                                children=[
                                    html.Img(src="/assets/team4.jpg", style={"width": "200px", 
        "height": "200px", 
        "borderRadius": "50%", 
        "objectFit": "cover"}),
                                    html.H4("Ruturaj Patond", style={"color": "#6a0dad", "marginTop": "10px"}),
                                    html.P("Marketing Head"),
                                ],
                            ), width=3
                        ),
                    ]
                ),
            ],
        ),

        # Contact Section with Form
        html.Div(
            id="contact",
            style={"padding": "50px", "backgroundColor": "#6a0dad", "color": "white"},
            children=[
                html.H2("Contact Us", style={"textAlign": "center", "marginBottom": "40px", "fontWeight": "bold"}),
                dbc.Row(
                    justify="center",
                    children=[
                        dbc.Col(
                            html.Div(
                                style={
                                    "maxWidth": "500px",
                                    "margin": "0 auto",
                                    "backgroundColor": "white",
                                    "padding": "20px",
                                    "borderRadius": "10px",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                                },
                                children=[
                                    dcc.Input(placeholder="Your Name", style={
                                        "width": "100%", "marginBottom": "15px", "padding": "10px", "borderRadius": "5px"
                                    }),
                                    dcc.Input(placeholder="Your Email", style={
                                        "width": "100%", "marginBottom": "15px", "padding": "10px", "borderRadius": "5px"
                                    }),
                                    dcc.Textarea(placeholder="Your Message", style={
                                        "width": "100%", "height": "100px", "marginBottom": "15px", "padding": "10px", "borderRadius": "5px"
                                    }),
                                    html.Button("Submit", style={
                                        "width": "50%", "padding": "10px", "backgroundColor": "#6a0dad", "color": "white",
                                        "border": "none", "borderRadius": "5px", "cursor": "pointer", "margin-left": "110px"
                                    }),
                                ],
                            ),
                            width=6,
                        ),
                    ],
                ),
            ],
        ),

        # Footer Section
        html.Div(
            style={
                "textAlign": "center",
                "padding": "20px",
                "backgroundColor": "#6a0dad",
                "color": "white"
            },
            children=[
                html.P("© 2025 ExcelXpert. Transforming spreadsheets into insights."),
            ],
        ),
    ],
)
