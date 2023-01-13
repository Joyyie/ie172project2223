import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Enter the details'),
        html.Hr(),
        dbc.Alert('Please supply details.', color="danger", id='signup_alert',
                  is_open=False),
        dbc.Row(
            [
                dbc.Label("First Name:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_firstname", placeholder="Enter your first name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Last Name:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_lastname", placeholder="Enter your last name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Contact Number:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_contactnumber", placeholder="+63"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Address:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_address", placeholder="Enter your address"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Sex:", width=2),
                dbc.Col(
                    dcc.Dropdown(
                        ['Female', 'Male', 'Others', 'Prefer Not to Respond'],
                        id='signup_gender'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Birthdate:", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='signup_birthdate'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_password", placeholder="Enter a password",
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label("Confirm Password:", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_passwordconf", placeholder="Re-type the password."
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button('Sign Up', color="secondary", id='singup_signupbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                dbc.ModalBody("User has been saved.", id='signup_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/home'
                    )
                ),
            ],
            id="signup_modal",
            is_open=False,
        ),
    ]
)


# disable the signup button if passwords do not match
@app.callback(
    [
        Output('singup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('singup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_firstname', 'value'),
        State('signup_lastname', 'value'),
        State('signup_password', 'value'),
        State('signup_contactnumber', 'value'),
        State('signup_address', 'value'),
        State('signup_gender', 'value'),
        State('signup_birthdate', 'date')
    ]
)
def saveuser(loginbtn, firstname, lastname, password, contactnumber, address, gender, birthdate):
    openalert = openmodal = False
    if loginbtn:
        if firstname and password:
            sql = """INSERT INTO users (
                user_firstname,
                user_lastname, 
                user_password, 
                user_number, 
                user_address, 
                user_gender, 
                user_birthdate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""  
            
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins should see
            # user passwords 
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [firstname, lastname, encrypt_string(password), contactnumber, address, gender, birthdate]
            db.modifydatabase(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]