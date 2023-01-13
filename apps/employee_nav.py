from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

from apps import signup

navlink_style = {
    'color': '#fff'
}

name = ""

navbar = dbc.Navbar(
    [
        dbc.Label(name),
        dbc.NavLink("Overview", href="/employee_home", style=navlink_style),
        dbc.NavLink("Transactions", href="/transactions_home", style=navlink_style),
        dbc.NavLink("Inventory", href="/inventory_home", style=navlink_style),
        dbc.NavLink("Employee", href="/employee_home/employee_profile", style=navlink_style),
        dbc.NavLink("Log Out", href="/home", style=navlink_style)
    ],
    dark=True,
    color='#E18AAA'
)