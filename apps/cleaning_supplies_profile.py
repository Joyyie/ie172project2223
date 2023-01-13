from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs
import pandas as pd

from app import app
from apps import dbconnect as db

from apps import employee_nav as en

layout = html.Div(
    [
        en.navbar,
        html.H2("Cleaning Supplies Details"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Supplies ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cleaning_supplies_id", placeholder="Enter ID"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Product Name", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='cleaning_supplies_name',
                            clearable=True,
                            searchable=True,
                        ), 
                        className="dash-bootstrap"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Description", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cleaning_supplies_description", placeholder="Enter Price"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Current Inventory", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="cleaning_supplies_inventory", placeholder="Enter Customer Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        html.Hr(),
        dbc.Button('Submit', color="secondary", id='cleaning_supplies_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='cleaning_supplies_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="cleaning_supplies_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="cleaning_supplies_modal",
            is_open=False,
        ),
    ]
)

@app.callback(
    [
        Output('cleaning_supplies_name', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def supplies_loaddropdown(pathname):
    
    if pathname == '/inventory_home/cleaning_supplies_home/cleaning_supplies_profile':
        sql = """
            SELECT supplies_name as label, supplies_id as value
            FROM supplies
            WHERE supplies_delete_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        supplies_opts = df.to_dict('records')
    
    else:
        raise PreventUpdate

    return [supplies_opts]