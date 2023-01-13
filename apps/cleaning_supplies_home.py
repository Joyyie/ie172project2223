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
    html.H2('CLEANING SUPPLIES', style={'top': '10px', 'font-weight': 'bold', 'text-align': 'center'}),
    html.Hr(),
    dbc.Card(
        [
            dbc.CardHeader(html.H4("Cleaning Supplies Management"
            )),
            dbc.CardBody(
                [
                    dbc.Button('Add Cleaning Supply', href = '/inventory_home/cleaning_supplies_home/add_supplies?mode=add', color = 'secondary'),
                    html.Div(
                        [
                        html.Br(),
                        html.Hr(),
                        dbc.Row(
                        [
                            dbc.Label("Search Cleaning Supply", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", id="supply_name_filter", placeholder="Enter filter"
                                ),
                                width=6,
                            )
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        "This will contain the table for supplies.",
                        id="supply_list"
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
        Output('supply_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('supply_name_filter', 'value')
    ]
)

def supply_loadlist(pathname, searchterm):
    if pathname == '/inventory_home/cleaning_supplies_home':
        sql = """SELECT 
                supply_name,
                supply_stock,
                supply_brand,
                supply_id
            FROM supplies
            WHERE NOT supply_delete_ind"""
        val = [] 
        colnames = ['Cleaning Supply', 'Stock', 'Brand', 'ID']

        if searchterm:
            sql += """ AND supply_name ILIKE %s"""
            val += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, val, colnames)
        
        if df.shape[0]: 
            buttons = []
            for supplyid in df ['ID']:
                 buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f'cleaning_supplies_home/add_supplies?mode=edit&id={supplyid}',
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