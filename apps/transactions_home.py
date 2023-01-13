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
    html.H2('TRANSACTIONS', style={'top': '10px', 'font-weight': 'bold', 'text-align': 'center'}),
    html.Hr(),
    dbc.Card(
        [
            dbc.CardHeader(html.H4("Transaction Management"
            )),
            dbc.CardBody(
                [
                    dbc.Button('Add Transaction', href = '/transactions_home/add_transactions?mode=add', color = 'secondary'),
                    html.Div(
                        [
                        html.Br(),
                        html.Hr(),
                        dbc.Row(
                        [
                            dbc.Label("Search Customer Name", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", id="cust_name_filter", placeholder="Enter filter"
                                ),
                                width=6,
                            )
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        "This will contain the table for transactions.",
                        id="transaction_list"
                    )
                    ]
                    ) 
                ]
            )
        ]
    )
    ]
)

@app.callback(
    [
        Output('transaction_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('cust_name_filter', 'value')
    ]
)

def transaction_loadlist(pathname, searchterm):
    if pathname == '/transactions_home':
        sql = """SELECT 
                customer_name,
                trans_date,
                service_name,
                trans_price,
                trans_status_name,
                trans_id
            FROM transactions
            WHERE NOT trans_delete_ind"""
        val = [] 
        colnames = ['Customer Name', 'Date of Transaction', 'Service', 'Price','Status', 'ID']

        if searchterm:
            sql += """ AND customer_name ILIKE %s"""
            val += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, val, colnames)
        
        if df.shape[0]: 
            buttons = []
            for transactionid in df ['ID']:
                 buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f'transactions_home/add_transactions?mode=edit&id={transactionid}',
                                size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            
            df['Action'] = buttons
            
        #     # remove the column ID before turning into a table 
            df.drop('ID', axis=1, inplace=True)
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["There are no records that match the search term."]
    else:
        raise PreventUpdate