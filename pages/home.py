#!/usr/bin/env python3
# coding: utf-8

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from flask_login import current_user

dash.register_page(__name__, path_template="/home", title="Home")


def layout():
    return dbc.Container(
        children=[
            dcc.Location(id="url_home", refresh=False),
            html.H1("Home"),
        ],
        style={"display": "block" if current_user and current_user.is_authenticated else "none"},
    )
