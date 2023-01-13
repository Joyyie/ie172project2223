from turtle import Turtle
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from numpy import clongfloat
import pandas as pd
from urllib.parse import urlparse, parse_qs
import re

from app import app
from apps import dbconnect as db

from apps import employee_nav as en

layout = html.Div(
    [
    en.navbar,
        html.Div(
            [
                dcc.Store(
                    id='user_toload',
                    storage_type='memory',
                    data=0
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H2("EMPLOYEE DETAILS"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("First Name:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", 
                        id="user_firstname", 
                        placeholder="Enter your first name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Last Name:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", 
                        id="user_lastname", 
                        placeholder="Enter your last name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Contact Number:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", 
                        id="user_number", 
                        placeholder="+63"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Address:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", 
                        id="user_address", 
                        placeholder="Enter your address"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Sex:", width=2),
                dbc.Col(
                    dcc.Dropdown(
                        [
                        'Female', 
                        'Male', 
                        'Others', 
                        'Prefer Not to Respond'
                        ],
                        id='user_gender'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Birthdate:", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='user_birthdate'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        html.Hr(),
        dbc.Button('Submit', color='secondary', id='edituser_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage",id='edituser_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="edituser_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="edituser_modal",
            is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('user_toload', 'data')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ],
)
def user_toload(pathname, search):
    if pathname == '/employee_home/employee_profile/ed_profile':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0

    else:
        raise PreventUpdate

    return [to_load]

@app.callback(
    [
        Output('edituser_modal', 'is_open'),
        Output('edituser_feedback_message', 'children'),
        Output('edituser_closebtn', 'href')
    ],
    [
        Input('edituser_submitbtn', 'n_clicks'),
        Input('edituser_closebtn', 'n_clicks')
    ],
    [
        State('user_firstname', 'value'),
        State('user_lastname', 'value'),
        State('user_number', 'value'),
        State('user_address', 'value'),
        State('user_gender', 'value'),
        State('user_birthdate', 'date'),
        State('url', 'search'),
    ]
)
def user_updateprocess(submitbtn, closebtn,
                            first, last, number, address,
                            gender, birthdate, 
                            search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'edituser_submitbtn' and submitbtn:
        openmodal = True

        # check if you have inputs
        inputs = [
            first, 
            last, 
            number, 
            address,
            gender, 
            birthdate, 
        ]

        # if erroneous inputs, raise prompt
        if not all(inputs):
            feedbackmessage = "Please supply all inputs."
        elif len(first)>255:
            feedbackmessage = "Name is too long."
        elif len(last)>255:
            feedbackmessage = "Name is too long."
        elif not str.isdigit(number):
            feedbackmessage = "Please enter a valid phone number."
        elif len(number)>10:
            feedbackmessage = "Phone number is too long (length>10)."
        elif len(number)<10:
            feedbackmessage = "Phone number is too short (length<10)."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'edit':
                parsed = urlparse(search)
                transid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE users
                SET
                    user_firstname = %s,
                    user_lastname = %s,
                    user_number = %s,
                    user_address = %s,
                    user_gender = %s,
                    user_birthdate = %s
                WHERE
                    user_id = %s
                """

                values = [first, last, number, address,
                            gender, birthdate, transid]
                
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Profile has been updated."
                okay_href = '/employee_home/employee_profile'

            else:
                raise PreventUpdate

    elif eventid == 'edituser_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]

@app.callback(
    [
        Output('user_firstname', 'value'),
        Output('user_lastname', 'value'),
        Output('user_number', 'value'),
        Output('user_address', 'value'),
        Output('user_gender', 'value'),
        Output('user_birthdate', 'date'),
    ],
    [
        Input('user_toload', 'modified_timestamp')
    ],
    [
        State('user_toload', 'data'),
        State('url', 'search'),
        State('currentuserid', 'data')
    ]
)
def user_loadprofile(timestamp, to_load, search, currentuserid):
    if to_load == 1:
        sql = """SELECT 
                user_firstname,
                user_lastname,
                user_number,
                user_address,
                user_gender,
                user_birthdate
            FROM users
            WHERE user_id = {}
            """.format(currentuserid)
        parsed = urlparse(search)
        userid = parse_qs(parsed.query)['id'][0]

        val = [userid]
        colnames = ['first','last','number','address','gender','birthdate']

        df = db.querydatafromdatabase(sql, val, colnames)

        first = df['first'][0]
        last = df['last'][0]
        number = df['number'][0]
        address = df['address'][0]
        gender = df['gender'][0]
        birthdate = df['birthdate'][0]
        return [first, last, number, address, gender, birthdate]

    else:
        raise PreventUpdate