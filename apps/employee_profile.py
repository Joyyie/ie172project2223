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
    html.H2('EMPLOYEE', style={'top': '10px', 'font-weight': 'bold', 'text-align': 'center'}),
    html.Hr(),
    dbc.Card(
        [
            dbc.CardHeader(html.H4("Employee List"
            )),
                    html.Div(
                        "This will contain the table for employees.",
                        id="employee_list"
                    )
                    ]
                    ) 
                ]
            )

@app.callback(
    [
        Output('employee_list', 'children'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('currentuserid', 'data')
    ]
)

def transaction_loadlist(pathname, currentuserid):
    if pathname == '/employee_home/employee_profile':
        sql = """SELECT 
                user_firstname,
                user_lastname,
                user_number,
                user_address,
                user_gender,
                user_birthdate,
                user_id
            FROM users
            WHERE user_id = {}
            """.format(currentuserid)
        val = [] 
        colnames = ['First Name', 'Last Name', 'Contact Number', 'Address', 'Sex', 'Birthdate', 'ID']

        df = db.querydatafromdatabase(sql, val, colnames)
        
        if df.shape[0]: 
            buttons = []
            for userid in df ['ID']:
                 buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'employee_profile/ed_profile?mode=edit&id={userid}',
                                size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            
            df['Action'] = buttons

            df.drop('ID', axis=1, inplace=True)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
    else:
        raise PreventUpdate