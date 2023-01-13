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
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("Transaction Status"),
                                html.Br(),
                                dbc.Card(
                                    id = "pending_transactions",
                                    className="mb-3"
                                )
                            ]
                        ),
                        dbc.Col(
                            [
                                html.H1("Current Supplies Inventory"),
                                html.Br(),
                                dbc.Card(
                                    id = "inventory_loadlist",
                                    className="mb-3"
                                )
                            ]
                        )
                    ],
                    className="g-0"
                ),
                html.Br(),
                html.Hr(),
                html.H1 ("Daily Summary"),
                html.Div(
                id="summary_loadlist"
            ),
            ]
        )
    ]
)


@app.callback(
    [
        Output('pending_transactions', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)

def transaction_loadlist(pathname):
    if pathname == '/employee_home':
        sql = """SELECT
                    trans_status_name,
                    COUNT(trans_id)
                FROM transactions
                GROUP BY
                    trans_status_name"""
        val = [] 
        colnames = ['Status','Number of Transactions']

        df = db.querydatafromdatabase(sql, val, colnames)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
        
        return [table]
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('summary_loadlist', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)

def summary_loadlist(pathname):
    if pathname == '/employee_home':
        sql = """SELECT
                    trans_date,
                    COUNT(trans_id),
                    SUM (trans_price)
                FROM transactions
                GROUP BY
                    trans_date"""
        val = [] 
        colnames = ['Date', 'Number of Transactions', 'Total Sales']

        df = db.querydatafromdatabase(sql, val, colnames)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
        
        return [table]
    else:
        raise PreventUpdate



@app.callback(
    [
        Output('inventory_loadlist', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)

def inventory_loadlist(pathname):
    if pathname == '/employee_home':
        sql = """SELECT
                    MAX(supply_id),
                    supply_name,
                    supply_stock
                FROM supplies
                GROUP BY supply_name, supply_stock"""
        val = [] 
        colnames = ['ID', 'Name', 'Inventory']

        df = db.querydatafromdatabase(sql, val, colnames)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
        
        return [table]
    else:
        raise PreventUpdate