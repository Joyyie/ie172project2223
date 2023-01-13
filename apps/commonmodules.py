from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate


navlink_style = {
    'color': '#000000',
    'font-family': 'Tahoma'
}

navbar = dbc.Navbar(
    [
        html.Img(src=r'assets/Logo.png', 
                        alt='image', 
                        height = 80, 
                        width = 80,
                        style = {
                            'left': '100px'
                        }
                        ),
        html.A(
            dbc.NavbarBrand("Clean-and-Go", className="ml-2", 
                            style={
                                'margin-right': '12em',
                                'color': '#000000',
                                'font-family': 'Tahoma',
                                'font-weight': 'bold',
                                'font-size': '30px'
                                }),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style={'font-size': '25px', 'color': '#000000'}),
        dbc.NavLink("About", href="/about_us", style={'font-size': '25px', 'color': '#000000'}),
        dbc.NavLink("Services", href="/services_offered", style={'font-size': '25px', 'color': '#000000'}),
        dbc.NavLink("Contact Us", href="/contact_us", style={'font-size': '25px', 'color': '#000000'}),
        dbc.NavLink("FAQS", href="/faqs", style={'font-size': '25px', 'color': '#000000'}),
        dbc.NavLink("Log-in / Sign-up", href="/log-in_sign-up", style={'font-size': '25px', 'color': '#000000'}),
    ],
    dark=True,
    color='#b4d1ce',
)