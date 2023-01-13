from dash import html

import dash_bootstrap_components as dbc

layout = html.Div(
    [
    html.Img(src=r'assets/Home.png', 
                        alt='image', 
                        height = 500, 
                        width = 500,
                        style = {
                            'position': 'absolute',
                            'top': '175px',
                            'left': '150px'
                        }
                        ),
    html.H1("Clean clothes. Clean life.",
            style = {
                'color': '#000000',
                'font-family': 'Verdana',
                'font-weight': 'bold',
                'font-size': '50px',
                'text-align': 'justify',
                'position': 'absolute',
                'top': '275px',
                'right': '150px',
                'height': '100px',
            }
            ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(
        [
            html.P(
                "You deserve a fresh start every day. We are here to provide you with the quality laundry service you need. ",
                style = {
                    'color': '#000000',
                    'font-family': 'arial',
                    'font-size': '20px',
                    'text-align': 'justify',
                    'position': 'absolute',
                    'top': '375px',
                    'right': '235px',
                    'height': '100px',
                    'width': '600px'
                }
            ),
            html.Br(),
            html.Br(),
            html.P(
                "Clean and go. Because you and your clothes deserve freshness.",
                style={
                    'color': '#000000',
                    'font-style':'italic',
                    'font-family': 'arial',
                    'font-size': '20px',
                    'text-align': 'justify',
                    'position': 'absolute',
                    'top': '475px',
                    'right': '235px',
                    'height': '100px',
                    'width': '600px'
                }
            ),
            html.A(
            dbc.Button('Contact Us!', color="#E18AAA", id='contact_us_contact_usbtn', href='/contact_us', style = {
            'color': '#E18AAA',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '20px',
            'position': 'absolute',
            'left': '685px',
            'width': '160px',
            'top':'550px'
        }
        ),
        ),
        ]
        )
    ]
)