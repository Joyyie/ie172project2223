from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from apps import dbconnect as db

from apps import employee_nav as en


layout = html.Div(
    [
    en.navbar,
    html.Br(),
    html.H2('INVENTORY', style={'top': '10px', 'font-weight': 'bold', 'text-align': 'center'}),
    html.Hr(),
    html.H2(),
    html.Div(
        [
            dbc.Card(
                    dbc.CardBody(
                        [    
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(src=r'assets/Supplies.png', 
                                            alt='fb_logo', 
                                            height = 300, 
                                            width = 250,
                                            style={
                                                'position': 'relative',
                                                'align':'center'
                                            },
                                        )
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Button('Cleaning Supplies', color="secondary", 
                                                            href = '/inventory_home/cleaning_supplies_home', 
                                                            style = {
                                                                    'justify': 'center',
                                                                    'align':'center',
                                                                    'width': '260px'
                                                            }
                                                        ),
                            html.Br(),
                        ]
                    ),
                    style={'width': "300px",
                           'height': '400px',
                           'position': 'absolute',
                           'justify': 'center',
                           'align': 'center',
                           'horizontal-align': 'middle',
                           'transform': 'translate(110%, 4%)',
                           'border': '10px solid rgba(0,0,0,0)'
                    }
                ),
            html.Div(
                [
                    dbc.Card(
                    dbc.CardBody(
                        [    
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(src=r'assets/Equipment.png', 
                                            alt='fb_logo', 
                                            height = 300, 
                                            width = 250,
                                            style={
                                                'position': 'relative',
                                                'align':'center'
                                            },
                                        )
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Button('Equipment', color = 'secondary', 
                                                    href = '/inventory_home/equipment_home', 
                                                    style = {
                                                        'justify': 'center',
                                                        'align':'center',
                                                        'width': '260px'
                                                        }
                                                    ),
                            html.Br(),
                        ]
                    ),
                    style={'width': "300px",
                           'height': '400px',
                           'position': 'absolute',
                           'justify': 'center',
                           'align': 'center',
                           'horizontal-align': 'middle',
                           'transform': 'translate(280%, 4%)',
                           'border': '10px solid rgba(0,0,0,0)'
                    }
                ),
                ]
            )
        ]
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    ]
)
