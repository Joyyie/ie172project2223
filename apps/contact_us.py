import dash_bootstrap_components as dbc
from dash import html

layout = html.Div(
    [
    html.H2('Contact Us',
        style = {
            'color': '#000000',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '40px',
            'text-align':'center',
            'position': 'center'
        }
        ),
    html.Hr(),
    html.H4('Have other concerns? You may reach us through:',
        style = {
            'color': '#000000',
            'font-family': 'Arial',
            'font-size': '20px',
            'text-align':'center',           
            'position': 'center'
        }
    ),

    html.Br(),
    
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Img(src=r'assets/FB.png', 
                            alt='fb_logo', 
                            height = 70, 
                            width = 70,
                            style = {
                                'top': '10px',
                                'position': 'relative',
                                'left': '105px',
                            }
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H6("Clean-and-Go Laundry Shop",
                                style = {
                                    'color': '#000000',
                                    'font-family': 'Arial',
                                    'font-weight': 'bold',
                                    'font-size': '20px',
                                    'text-align': 'center'
                                }
                            ),
                            html.P("facebook.com/clean-and-go-laundry-shop",
                            style = {
                                    'color': '#000000',
                                    'font-family': 'Arial',
                                    'font-size': '16px',
                                    'text-align': 'center'
                                }
                            ),
                        ]
                    ),
                    style={"width": "20rem",
                            'height': '15rem'
                    }
                ),    
                width=3),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Img(src=r'assets/Phone.png', 
                            alt='phone_icon', 
                            height = 70, 
                            width = 70,
                            style = {
                                'top': '10px',
                                'position': 'relative',
                                'left': '105px',
                            }
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H6("123-4567",
                                style = {
                                    'color': '#000000',
                                    'font-family': 'Arial',
                                    'font-weight': 'bold',
                                    'font-size': '20px',
                                    'text-align': 'center'
                                }
                            )
                        ]
                    ),
                    style={"width": "20rem",
                            'height': '15rem'
                        }
                ), 
                width=3),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Img(src=r'assets/GMail.png', 
                            alt='email_icon', 
                            height = 70, 
                            width = 70,
                            style = {
                                'top': '10px',
                                'position': 'relative',
                                'left': '105px',
                            }
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H6("clean_and_go@gmail.com",
                                style = {
                                    'color': '#000000',
                                    'font-family': 'Arial',
                                    'font-weight': 'bold',
                                    'font-size': '20px',
                                    'text-align': 'center'
                                }
                            )
                        ]
                    ),
                    style={"width": "20rem",
                            'height': '15rem'
                            }
                ),    
                width=3),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Img(src=r'assets/Location.png', 
                            alt='location_icon', 
                            height = 70, 
                            width = 70,
                            style = {
                                'top': '10px',
                                'position': 'relative',
                                'left': '105px',
                            }
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H6(" Lt. J. Francisco St., Krus na Ligas, Diliman, Kyusi",
                                style = {
                                    'color': '#000000',
                                    'font-family': 'Arial',
                                    'font-weight': 'bold',
                                    'font-size': '17px',
                                    'text-align': 'center'
                                }
                            )
                        ]
                    ),
                    style={"width": "20rem",
                           'height': '15rem'
                            }
                ),
                width=3)
            ]
        ) 
    ]
)

######################

# first_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H5("Card title", className="card-title"),
#             html.P("This card has some text content, but not much else"),
#             dbc.Button("Go somewhere", color="primary"),
#         ]
#     )
# )


# second_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H5("Card title", className="card-title"),
#             html.P(
#                 "This card also has some text content and not much else, but "
#                 "it is twice as wide as the first card."
#             ),
#             dbc.Button("Go somewhere", color="primary"),
#         ]
#     )
# )


# cards = dbc.Row(
#     [
#         dbc.Col(first_card, width=4),
#         dbc.Col(second_card, width=8),
#     ]
# )