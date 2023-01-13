from dash import html

layout = (html.Div([
    html.Img(src=r'assets/AU1.png', 
                        alt='image', 
                        height = 300, 
                        width = 300,
                        style = {
                            'position': 'absolute',
                            'top': '125px',
                            'left': '75px'
                        }
                        ),
    html.H2('About Us',
        style = {
            'color': '#000000',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '50px',
            'text-align': 'left',
            'position': 'absolute',
            'left': '400px',
            'top': '150px'
            }
                ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P("Clean-and-Go is a laundry shop that provides top-notch laundry services in the local community. Opened in 2017, it has been consistently providing freshness to its customers, one cloth at a time. It is the leading laundry service in the local community having been ranked as the best choice among its competitors for three consecutive years. It is located in Lt. J. Francisco St., Krus na Ligas, Diliman, Quezon City.",
        style = {
            'color': '#000000',
            'font-family': 'Arial',
            'font-size': '20px',
            'text-align': 'left',
            'position': 'absolute',
            'left': '400px',
            'top': '225px',
            'width': '975px'
            }
        )
    ]
),
html.Span([
    html.Img(src=r'assets/AU2.png', 
                        alt='image', 
                        height = 300, 
                        width = 300,
                        style = {
                            'position': 'absolute',
                            'top': '400px',
                            'right': '125px'
                        }
                        ),
    html.H2('Mission',
        style = {
            'color': '#000000',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '50px',
            'text-align': 'right',
            'position': 'absolute',
            'right': '450px',
            'top': '400px'
        }
        ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P("To provide its customers with a consistent high quality laundry service that will give them a sense of comfort and freshness they need in life.",
        style = {
            'color': '#000000',
            'font-family': 'Arial',
            'font-size': '20px',
            'text-align': 'left',
            'position': 'absolute',
            'left': '125px',
            'top': '475px',
            'width': '975px'
        }
        )
    ]
),
html.Div([
    html.Img(src=r'assets/AU3.png', 
                        alt='image', 
                        height = 300, 
                        width = 300,
                        style = {
                            'position': 'absolute',
                            'top': '675px',
                            'left': '100px'
                        }
                        ),
    html.H2('Vision',
        style = {
            'color': '#000000',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '50px',
            'text-align': 'left',
            'position': 'absolute',
            'left': '400px',
            'top': '675px'
        }
        ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P("Clean-and-Go is the leading laundry shop with multiple branches scattered around Quezon City.",
        style = {
            'color': '#000000',
            'font-family': 'Arial',
            'font-size': '20px',
            'text-align': 'left',
            'position': 'absolute',
            'left': '400px',
            'top': '750px',
            'width': '975px'
        }
        )
    ]
))