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
                    id='equip_toload',
                    storage_type='memory',
                    data=0
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H2("EQUIPMENT DETAILS"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Equipment Name:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="equip_name",
                        placeholder="Enter Equipment Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Status:", width=2),
                dbc.Col(
                    dcc.Dropdown(
                        [
                            'Idle',
                            'In Use',
                            'Under Maintenance'
                            ],
                        id='equip_status'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Maintenance Date:", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='equip_date',
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Brand:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="equip_brand",
                        placeholder="Enter Equipment Brand"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        html.Div(
                dbc.Row(
                [
                    dbc.Label("Wish to Delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='equip_removerecord',
                            options=[
                                {
                                'label': "Mark for Deletion",
                                'value': 1
                                }
                            ],
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='equip_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='secondary', id='addingequip_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage",id='addingequip_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="addingequip_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="addingequip_modal",
            is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('equip_toload', 'data'),
        Output('equip_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ],
)
def equip_toload(pathname, search):
    if pathname == '/inventory_home/equipment_home/add_equipment':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}

    else:
        raise PreventUpdate

    return [to_load, removerecord_div]

@app.callback(
    [
        Output('addingequip_modal', 'is_open'),
        Output('addingequip_feedback_message', 'children'),
        Output('addingequip_closebtn', 'href')
    ],
    [
        Input('addingequip_submitbtn', 'n_clicks'),
        Input('addingequip_closebtn', 'n_clicks')
    ],
    [
        State('equip_name', 'value'),
        State('equip_status', 'value'),        
        State('equip_date', 'date'),
        State('equip_brand', 'value'),
        State('url', 'search'),
        State('equip_removerecord', 'value'),
    ]
)
def equip_submitprocess(submitbtn, closebtn,

                            name, status, date, brand, 
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'addingequip_submitbtn' and submitbtn:
        openmodal = True

        # check if you have inputs
        inputs = [
            name,
            status,
            brand
        ]

        # if erroneous inputs, raise prompt
        if not all(inputs):
            feedbackmessage = "Please supply all inputs."
        elif len(name)>255:
            feedbackmessage = "Name is too long."
        elif len(brand)>255:
            feedbackmessage = "Brand is too long."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':
                # save to db
                sqlcode = """ INSERT INTO equip(
                    equip_name,
                    equip_status,
                    equip_date,
                    equip_brand
                )
                VALUES (%s, %s, %s, %s)
                """
                values = [name, status, date, brand]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Equipment has been recorded."
                okay_href = '/inventory_home/equipment_home'
            
            elif mode == 'edit':
                parsed = urlparse(search)
                equipid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE equip
                SET
                    equip_name = %s,
                    equip_status = %s,
                    equip_date = %s,
                    equip_brand = %s,
                    equip_delete_ind = %s
                WHERE
                    equip_id = %s
                """
                to_delete = bool(removerecord)

                values = [name, status, date, brand, to_delete, equipid]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Equipment has been updated."
                okay_href = '/inventory_home/equipment_home'

            else:
                raise PreventUpdate

    elif eventid == 'addingequip_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]

@app.callback(
    [
        Output('equip_name', 'value'),
        Output('equip_status', 'value'),
        Output('equip_date', 'date'),
        Output('equip_brand', 'value'),
    ],
    [
        Input('equip_toload', 'modified_timestamp')
    ],
    [
        State('equip_toload', 'data'),
        State('url', 'search'),
    ]
)
def add_equip_loadprofile(timestamp, to_load, search):
    if to_load == 1:
        sql = """SELECT 
                equip_name,
                equip_status,
                equip_date,
                equip_brand
            FROM equip
            WHERE equip_id = %s
            """
        parsed = urlparse(search)
        equipid = parse_qs(parsed.query)['id'][0]

        val = [equipid]
        colnames = ['name', 'status', 'date', 'brand']

        df = db.querydatafromdatabase(sql, val, colnames)

        name = df['name'][0]
        status = df['status'][0]
        date = df['date'][0]
        brand = df['brand'][0]

        return [name, status, date, brand]

    else:
        raise PreventUpdate