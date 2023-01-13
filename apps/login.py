import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Alert('Employee ID or password is incorrect.', color="danger", id='login_alert',
                  is_open=False),
        html.Div([
            dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(src=r'assets/Logo.png', 
                                            alt='fb_logo', 
                                            height = 450, 
                                            width = 450,
                                            style={
                                                'position': 'relative',
                                                'align':'center'
                                            }
                                        ),
                                    ),
                                ],
                                className="mb-3",
                            ),
                        ]
                    ),
                    style={'width': "475px",
                           'height': '475px',
                           'position': 'absolute',
                           'justify': 'center',
                           'align': 'center',
                           'horizontal-align': 'middle',
                           'transform': 'translate(50%, 0%)',
                           'border': '10px solid rgba(0,0,0,0)'
                    }
                ),
            dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3('Log-In / Sign-Up', style={'text-align':'center'}),
                            html.Hr(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                                    
                            dbc.Row(
                                [
                                    
                                    html.Br(),
                                    dbc.Col(
                                        dbc.Input(
                                            type="text", id="login_id", placeholder="Employee ID", style={'text-align': 'center'},
                                            value=''
                                        ),
                                        style = {
                                            'text-align':'center',
                                            'justify': 'center',
                                            'align': 'center',
                                            'border-radius': '5%'
                                        },
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Input(
                                            type="password", id="login_password", placeholder="Enter password", style={'text-align': 'center'}
                                        ),
                                        style = {
                                            'text-align':'center',
                                            'justify': 'center',
                                            'align': 'center'
                                        },
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Button('Login', color="secondary", id='login_loginbtn', style={'class':'rounded-pill', 'width':'260px'}),
                            html.Hr(),
                            html.A('Signup Now!', href='/signup'),
                            html.Br(),
                        ]
                    ),
                    style={'width': "300px",
                           'height': '475px',
                           'position': 'absolute',
                           'justify': 'center',
                           'align': 'center',
                           'horizontal-align': 'middle',
                           'transform': 'translate(250%, 4%)',
                    }
                ),
                ]
                )
    ]
)

@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks')
    ],
    [
        State('login_id', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
    ]
)
def loginprocess(loginbtn, id, password,
                 sessionlogout, currentuserid):
    openalert = False
    if loginbtn and id and password:
        sql = """SELECT user_id
        FROM users
        WHERE 
            user_id = %s AND
            user_password = %s AND
            NOT user_delete_ind
            """
        # we match the encrypted input to the encrypted password in the db
        encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
         
        values = [id, encrypt_string(password)]
        cols = ['userid']
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape[0]: # if query returns rows
            currentuserid = df['userid'][0]
        else:
            currentuserid = -1
            openalert = True
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'), 
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/employee_home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]