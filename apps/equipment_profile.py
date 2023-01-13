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
        html.H2("Equipment Details"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Equipment ID", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="equipment_id", placeholder="Enter ID"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Maintenance Schedule", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='equipment_schedule'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Equipment Type", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='equipment_type',
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
        html.Hr(),
        dbc.Button('Submit', color="secondary", id='equipment_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='equipment_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="equipment_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="equipment_modal",
            is_open=False,
        ),
    ]
)

@app.callback(
    [
        Output('equipment_type', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def type_loaddropdown(pathname):
    
    if pathname == '/inventory_home/equipment_home/equipment_profile':
        sql = """
            SELECT equipment_type as label, equipment_id as value
            FROM equipment
            WHERE equipment_delete_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        equipment_opts = df.to_dict('records')
    
    else:
        raise PreventUpdate

    return [equipment_opts]