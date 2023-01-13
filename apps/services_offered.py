from dash import html

layout = (html.Div(
    [
    html.H2('Services Offered',
        style = {
            'color': '#000000',
            'font-family': 'Verdana',
            'font-weight': 'bold',
            'font-size': '40px',
            'text-align': 'center',
            'position': 'center'
            }
                ),
    html.Hr(),
    html.Div(
        [
            html.Img(src=r'assets/Self Service.png', 
                        alt='image', 
                        height = 720, 
                        width = 1200,
                        style = {
                            'top': '250px',
                            'position': 'absolute',
                            'left': '160px'
                        }
                        ),
    html.Div(
        [
        html.Img(src=r'assets/Dry Cleaning.png', 
                        alt='image', 
                        height = 720, 
                        width = 1200,
                        style = {
                            'top': '1020px',
                            'position': 'absolute',
                            'left': '160px'
                        }
                        ),
    html.Div(
        [
            html.Img(src=r'assets/Drop Off.png', 
                        alt='image', 
                        height = 720, 
                        width = 1200,
                        style = {
                            'top': '1790px',
                            'position': 'absolute',
                            'left': '160px'
                        }
                        ),
        ]
    )
        ]
    )
        ]
        )
    ]
)
)