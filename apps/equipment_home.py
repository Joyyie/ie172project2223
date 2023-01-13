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
    html.H2('EQUIPMENT', style={'top': '10px', 'font-weight': 'bold', 'text-align': 'center'}),
    html.Hr(),
    dbc.Card(
        [
            dbc.CardHeader(html.H4("Equipment Management"
            )),
            dbc.CardBody(
                [
                    dbc.Button('Add Equipment', href = '/inventory_home/equipment_home/add_equipment?mode=add', color = 'secondary'),
                    html.Div(
                        [
                        html.Br(),
                        html.Hr(),
                        dbc.Row(
                        [
                            dbc.Label("Search Equipment", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", id="equip_name_filter", placeholder="Enter filter"
                                ),
                                width=6,
                            )
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        "This will contain the table for the equipment.",
                        id="equip_list"
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
        Output('equip_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('equip_name_filter', 'value')
    ]
)

def equip_loadlist(pathname, searchterm):
    if pathname == '/inventory_home/equipment_home':
        sql = """SELECT 
                equip_id,
                equip_name,
                equip_status,
                equip_brand,
                equip_date
            FROM equip
            WHERE NOT equip_delete_ind"""
        val = [] 
        colnames = ['ID', 'Equipment', 'Status', 'Brand', 'Maintenance Date']

        if searchterm:
            sql += """ AND equip_name ILIKE %s"""
            val += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, val, colnames)
        
        if df.shape[0]: 
            buttons = []
            for equipid in df ['ID']:
                 buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f'equipment_home/add_equipment?mode=edit&id={equipid}',
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