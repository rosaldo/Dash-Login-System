#!/usr/bin/env python3
# coding: utf-8

import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path_template="/", redirect_from=["/login"], title="Login")


def layout():
    return dbc.Container(
        children=[
            dbc.Col(
                children=[
                    dbc.Row(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("login"),
                                dbc.Input(
                                    id="login_name",
                                    tabindex=0,
                                    placeholder="Enter your login",
                                    type="email",
                                ),
                            ],
                        ),
                        style={"margin-top": "100px"},
                    ),
                    dbc.Row(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("password"),
                                dbc.Input(
                                    id="login_password",
                                    tabindex=1,
                                    placeholder="Enter your password",
                                    type="password",
                                ),
                            ],
                            style={"margin-top": "10px", "margin-bottom": "10px"},
                        ),
                    ),
                    dbc.Button(
                        id="login_button",
                        children="L O G I N",
                        n_clicks=0,
                        type="submit",
                        style={"width": "100%", "margin": "0px"},
                    ),
                    html.Table(
                        children=[
                            html.Tr(children=[html.Th("user:"), html.Td("thebestclient@mail.com")]),
                            html.Tr(children=[html.Th("password:"), html.Td("BestPass")]),
                        ],
                        style={"margin-top": "30px"},
                    ),
                ],
                class_name="d-grid gap-2 col-3 mx-auto",
            ),
        ],
    )
