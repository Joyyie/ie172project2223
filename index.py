from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps import home
from apps import about_us
from apps import services_offered
from apps import contact_us
from apps import faqs
from apps import login
from apps import signup
from apps import employee_home
from apps import transactions_home
from apps import add_transactions
from apps import inventory_home
from apps import cleaning_supplies_home
from apps import add_supplies
from apps import equipment_home
from apps import add_equipment
from apps import employee_profile
from apps import ed_profile

CONTENT_STYLE = {
    #edit for designs"
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        cm.navbar,
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output('page-content', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)
def displaypage(pathname):
    
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    if eventid == 'url':
        if pathname in ['/', '/home']:
            returnlayout = home.layout   
        
        elif pathname == '/about_us':
            returnlayout = about_us.layout
        #Make about_us layout

        elif pathname == '/services_offered':
            returnlayout = services_offered.layout
        #Make services_offered layout
        
        elif pathname == '/log-in_sign-up':
            returnlayout = login.layout
        #Make log-in_sign-up layout

        elif pathname == '/contact_us':
            returnlayout = contact_us.layout
        #Make contact_us layout

        elif pathname == '/faqs':
            returnlayout = faqs.layout
        #Make faqs.layout

        elif pathname == '/signup':
            returnlayout = signup.layout

        elif pathname == '/employee_home':
            returnlayout = employee_home.layout
        
        elif pathname == '/transactions_home':
            returnlayout = transactions_home.layout
        
        elif pathname == '/transactions_home/add_transactions':
            returnlayout = add_transactions.layout
        
        elif pathname == '/inventory_home':
            returnlayout = inventory_home.layout
        
        elif pathname == '/inventory_home/cleaning_supplies_home':
            returnlayout = cleaning_supplies_home.layout
        
        elif pathname == '/inventory_home/cleaning_supplies_home/add_supplies':
            returnlayout = add_supplies.layout

        elif pathname == '/inventory_home/equipment_home':
            returnlayout = equipment_home.layout
        
        elif pathname == '/inventory_home/equipment_home/add_equipment':
            returnlayout = add_equipment.layout

        elif pathname == '/employee_home/employee_profile':
            returnlayout = employee_profile.layout

        elif pathname == '/employee_home/employee_profile/ed_profile':
            returnlayout = ed_profile.layout
            
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
    return [returnlayout]



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)