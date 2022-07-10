#!/usr/bin/env python3
# coding: utf-8

import os
import secrets

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html, page_container
from flask import Flask
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from pages.client_db import Client, DBase, db

base = DBase()
server = Flask(__name__)
server.config.update(
    SECRET_KEY=secrets.token_hex(24),
    SQLALCHEMY_DATABASE_URI=base.db_name,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(server)
login_manager = LoginManager()
login_manager.init_app(server)

app = Dash(
    __name__,
    server=server,
    title="Dash Login System",
    update_title="Refreshing Dash Login System ...",
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.SKETCHY],
    meta_tags=[
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"},
    ],
)

brand_bar = dbc.Col(
    children=[
        dbc.Row(
            html.H1(
                children=[
                    dcc.Link(
                        children="DASH Login System - DASHBOARD",
                        href="/home",
                        style={"text-decoration": "none"},
                    )
                ],
                style={"text-align": "center"},
            ),
        ),
    ],
    class_name="d-grid gap-2 col-6 mx-auto",
)

nav_bar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("CREATE", href="/create")),
        dbc.NavItem(dbc.NavLink("READ", href="/read")),
        dbc.NavItem(dbc.NavLink("UPDATE", href="/update")),
        dbc.NavItem(dbc.NavLink("DELETE", href="/delete")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(
                    "LOGOUT",
                    href="#",
                    id="logout_button",
                    n_clicks=0,
                ),
            ],
            nav=True,
            in_navbar=True,
            id="mn_login",
        ),
    ],
    id="dashboard_menu",
    fluid=True,
    links_left=True,
    style={"display": "none"},
)

app.layout = dbc.Container(
    children=[
        dcc.Store(id="session", storage_type="session"),
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="url_logout", refresh=False),
        brand_bar,
        nav_bar,
        page_container,
    ],
    id="root",
    fluid=True,
    style={"margin": "0px", "padding": "0px"},
)


@login_manager.user_loader
def load_user(client_id):
    return Client.query.get(int(client_id))


@app.callback(
    [
        Output("mn_login", "label"),
        Output("dashboard_menu", "style"),
        Output("url", "pathname"),
        Output("url", "refresh"),
    ],
    Input("root", "loading_state"),
)
def set_enviroment(load_st):
    if current_user and not current_user.is_authenticated:
        return ["", {"display": "none"}, "/login", True]
    elif current_user and current_user.is_authenticated:
        return [current_user.email, {"display": "block"}, "/home", True]
    else:
        return ["", {"display": "none"}, "", False]


@app.callback(
    [
        Output("url_login", "pathname"),
        Output("url_login", "refresh"),
    ],
    Input("login_button", "n_clicks"),
    [
        State("login_name", "value"),
        State("login_password", "value"),
    ],
)
def set_login(bt_log, login, passwd):
    client = Client.query.filter_by(email=login).first()
    url = ["/login", True]
    if not client:
        return url
    elif not check_password_hash(client.passwd, passwd):
        return url
    else:
        login_user(client, remember=True)
        url = ["/home", True]
        return url


@app.callback(
    [
        Output("url_logout", "pathname"),
        Output("url_logout", "refresh"),
    ],
    Input("logout_button", "n_clicks"),
)
def set_logout(bt_logout):
    if bt_logout:
        logout_user()
        return ["/login", True]
    else:
        return ["", False]


self_name = os.path.basename(__file__)[:-3]
if len(os.sys.argv) == 1:
    app.run(host="127.0.0.1", port="8888", debug=True)
elif len(os.sys.argv) == 2:
    host = os.sys.argv[1]
    os.system(f"gunicorn {self_name}:server -b {host}:8888 --reload --timeout 120")
elif len(os.sys.argv) == 3:
    host = os.sys.argv[1]
    port = int(os.sys.argv[2])
    os.system(f"gunicorn {self_name}:server -b {host}:{port} --reload --timeout 120")
