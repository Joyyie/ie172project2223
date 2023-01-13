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
                    id='supply_toload',
                    storage_type='memory',
                    data=0
                )
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H2("CLEANING SUPPLY DETAILS"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Cleaning Supply Name:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="supply_name",
                        placeholder="Enter Cleaning Supply Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Stock:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="supply_stock",
                        placeholder="Enter Current Stock"
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
                        id="supply_brand",
                        placeholder="Enter Supply Brand"
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
                            id='supply_removerecord',
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
            id='supply_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Submit', color='secondary', id='addingsupply_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage",id='addingsupply_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="addingsupply_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="addingsupply_modal",
            is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('supply_toload', 'data'),
        Output('supply_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ],
)
def supply_toload(pathname, search):
    if pathname == '/inventory_home/cleaning_supplies_home/add_supplies':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}

    else:
        raise PreventUpdate

    return [to_load, removerecord_div]

@app.callback(
    [
        Output('addingsupply_modal', 'is_open'),
        Output('addingsupply_feedback_message', 'children'),
        Output('addingsupply_closebtn', 'href')
    ],
    [
        Input('addingsupply_submitbtn', 'n_clicks'),
        Input('addingsupply_closebtn', 'n_clicks')
    ],
    [
        State('supply_name', 'value'),
        State('supply_stock', 'value'),
        State('supply_brand', 'value'),
        State('url', 'search'),
        State('supply_removerecord', 'value'),
    ]
)
def supply_submitprocess(submitbtn, closebtn,

                            name, stock, brand, 
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'addingsupply_submitbtn' and submitbtn:
        openmodal = True

        # check if you have inputs
        inputs = [
            name, 
            stock,
            brand
        ]

        # if erroneous inputs, raise prompt
        if not all(inputs):
            feedbackmessage = "Please supply all inputs."
        elif len(name)>255:
            feedbackmessage = "Cleaning Supply Name is too long."
        elif len(brand)>255:
            feedbackmessage = "Brand is too long."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':
                # save to db
                sqlcode = """ INSERT INTO supplies(
                    supply_name,
                    supply_stock,
                    supply_brand
                )
                VALUES (%s, %s, %s)
                """
                values = [name, stock, brand]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Cleaning supply has been recorded."
                okay_href = '/inventory_home/cleaning_supplies_home'
            
            elif mode == 'edit':
                parsed = urlparse(search)
                supplyid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE supplies
                SET
                    supply_name = %s,
                    supply_stock = %s,
                    supply_brand = %s,
                    supply_delete_ind = %s
                WHERE
                    supply_id = %s
                """
                to_delete = bool(removerecord)

                values = [name, stock, brand, to_delete, supplyid]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Cleaning supply has been updated."
                okay_href = '/inventory_home/cleaning_supplies_home'

            else:
                raise PreventUpdate

    elif eventid == 'addingsupply_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]

@app.callback(
    [
        Output('supply_name', 'value'),
        Output('supply_stock', 'value'),
        Output('supply_brand', 'value'),
    ],
    [
        Input('supply_toload', 'modified_timestamp')
    ],
    [
        State('supply_toload', 'data'),
        State('url', 'search'),
    ]
)
def add_supply_loadprofile(timestamp, to_load, search):
    if to_load == 1:
        sql = """SELECT 
                supply_name,
                supply_stock,
                supply_brand
            FROM supplies
            WHERE supply_id = %s
            """
        parsed = urlparse(search)
        supplyid = parse_qs(parsed.query)['id'][0]

        val = [supplyid]
        colnames = ['name', 'stock', 'brand']

        df = db.querydatafromdatabase(sql, val, colnames)

        name = df['name'][0]
        stock = df['stock'][0]
        brand = df['brand'][0]

        return [name, stock, brand]

    else:
        raise PreventUpdate