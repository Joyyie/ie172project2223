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

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(
                    id='trans_toload',
                    storage_type='memory',
                    data=0
                )
            ]
        ),
        html.H2("Transaction Details"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Customer Name: ", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="customer_name",
                        placeholder="Enter Customer's Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Date of Transactions", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='trans_date',
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Service:", width=2),
                dbc.Col(
                    dcc.Dropdown(
                        [
                            'Self-Service', 
                            'Dry-Cleaning', 
                            'Drop-Off'],
                        id='service_name'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Price:", width=2),
                dbc.Col(
                    dbc.Input(
                                type="text", 
                                id="trans_price", 
                                placeholder="Enter Price"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Employee ID", width=2),
                dbc.Col(
                    dbc.Input(
                                type="text", 
                                id="user_id", 
                                placeholder="Enter Customer ID"
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
                                'Pending', 
                                'Ongoing', 
                                'Done'
                        ],
                        id='trans_status_name'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        # html.Div(
        #         dbc.Row(
        #         [
        #             dbc.Label("Wish to Delete?", width=2),
        #             dbc.Col(
        #                 dbc.Checklist(
        #                     id='employeeprof_removerecord',
        #                     options=[
        #                         {
        #                         'label': "Mark for Deletion",
        #                         'value': 1
        #                         }
        #                     ],
        #                     # I want the label to be bold
        #                     style={'fontWeight':'bold'},
        #                 ),
        #                 width=6,
        #             ),
        #         ],
        #         className="mb-3",
        #     ),
        #     id='employeeprof_removerecord_div'
        # ),
        html.Hr(),
        dbc.Button('Submit', color='secondary', id='addingtransaction_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage",id='addingtransaction_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="addingtransaction_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="addingtransaction_modal",
            is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('trans_toload', 'data'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
    ],
)
def trans_toload(pathname, search):
    if pathname == '/transactions_home/add_transactions':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0

    else:
        raise PreventUpdate
    return [to_load]

@app.callback(
    [
        Output('addingtransaction_modal', 'is_open'),
        Output('addingtransaction_feedback_message', 'children'),
    ],
    [
        Input('addingtransaction_submitbtn', 'n_clicks'),
        Input('addingtransaction_closebtn', 'n_clicks')
    ],
    [
        State('customer_name', 'value'),
        State('trans_date', 'date'),
        State('service_name', 'value'),
        State('trans_price', 'value'),
        State('user_id', 'value'),
        State('trans_status_name', 'value'),
        State('url', 'search')
    ]
)
def employeeprof_submitprocess(submitbtn, closebtn,

                            customer, date, service, 
                            price, employee, status, 
                            search):
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
    else:
        raise PreventUpdate
    
    if eventid == 'addingtransaction_submitbtn' and submitbtn:
        openmodal = True

        # check if you have inputs
        inputs = [
            customer,
            date,
            service,
            price,
            employee,
            status
        ]

        # if erroneous inputs, raise prompt
        if not all(inputs):
            feedbackmessage = "Please supply all inputs."
        elif len(customer)>255:
            feedbackmessage = "Name is too long."
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':
                sqlcode = """ INSERT INTO employees(
                    customer_name,
                    trans_date,
                    service_name,
                    trans_price,
                    user_id,
                    trans_status_name
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = [customer, date, service, price, employee, status]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Transaction has been saved."
            
            elif mode == 'edit':
                parsed = urlparse(search)
                transid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE employees
                SET
                    customer_name = %s,
                    trans_date = %s,
                    service_name = %s,
                    trans_price = %s,
                    user_id = %s,
                    trans_status_name = %s
                WHERE
                    transaction_id = %s
                """
                # to_delete = bool(removerecord)

                values = [customer, date, service, price, employee, status, transid]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Transaction has been updated."

            else:
                raise PreventUpdate

    elif eventid == 'addingtransaction_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage]


# get info from database (for editing)
@app.callback(
    [
        Output('customer_name', 'value'),
        Output('trans_date', 'date'),
        Output('service_name', 'value'),
        Output('trans_price', 'value'),
        Output('user_id', 'value'),
        Output('trans_status_name', 'value'),
    ],
    [
        Input('trans_toload', 'modified_timestamp')
    ],
    [
        State('trans_toload', 'data'),
        State('url', 'search'),
    ]
)
def add_transactions_loadprofile(timestamp, to_load, search):
    if to_load == 1:
        sql = """SELECT 
                    customer_name,
                trans_date,
                service_name,
                trans_price,
                user_id,
                trans_status_name,
            FROM transactions
            WHERE trans_id = %s
            """
        parsed = urlparse(search)
        transid = parse_qs(parsed.query)['id'][0]

        val = [transid]
        colnames = ['customer', 'date', 'service', 'price','employee','status']

        df = db.querydatafromdatabase(sql, val, colnames)

        # 2. load the values to the interface
        customer = df['customer'][0]
        date = df['date'][0]
        service = df['service'][0]
        price = int(df['price'][0])
        employee = int(df['employee'][0])
        status = df['status'][0]

        return [customer, date, service, price, employee, status]

    else:
        raise PreventUpdate
