"""monitor_page.py

Function for Generating Monitor Page and Creating Callback

"""

import dash

try:
    from dash import dcc
except:
    import dash_core_components as dcc

import dash_bootstrap_components as dbc

try:
    from dash import html
except:
    import dash_html_components as html

from dash.exceptions import PreventUpdate

from dash.dependencies import Input, Output, State

from flask_login import login_user, logout_user, current_user

from pathlib import Path
from time import time
from ..messaging.user import Users
from werkzeug.security import generate_password_hash, check_password_hash


def generate_layout():
    """Generates the Basic Layout for the Monitor Page

    Returns
    -------
    layout: html.div
        Monitor Page Layout
    """
    # TODO make layout generic, have divs for create and login
    
    layout = html.Div([dcc.Location(id="url_login", refresh=True)
            , html.Div(id="hidden_for_redirect")
            , html.H2("""Please log in to continue:""", id="h1")
            , dcc.Input(placeholder="Enter your email",
                    type="text",
                    id="email-box")
            , dcc.Input(placeholder="Enter your password",
                    type="password",
                    id="pw-box")
            , html.Button(children="Login",
                    n_clicks=0,
                    type="submit",
                    id="login-button")
            , html.Div(children="", id="status-div"),
            # TODO rename:
            html.Div(children="", id="new-div"),
            html.Div([html.H4("Don\'t have an account?"), 
                    html.Button("Click here to Create", 
                                n_clicks=0,
                                id="create-button")])
        ]) #end div
    return layout


# def register_callbacks(app, config, users_db):
def register_callbacks(app, users_db):
    """Registers the Callbacks for the Login Page
    # TODO type hinting
    Parameters
    ----------
    app : Dash Object
        Dash Object to Set Up Callbacks to
    config : dict
        Contains All Settings for Dashboard / Daemon
    users_db: SQLAlchemy db Object for user data handling    
    Returns
    -------
    None
    """


    # TODO remove "account not found" when re-entering information
    # TODO create callback

    @app.callback(
    [Output('container-button-basic', "children")]
    , [Input('create-button', 'n_clicks')]
    , [State('name', 'value'), State('email', 'value'), State('password', 'value')
    , State("create-button", "n-clicks")])
    def insert_users(_n, name, em, pw, n_clicks):
        # if n_clicks is None:
        #     print("n_clicks is none")
        #     raise dash.exceptions.PreventUpdate
        # else:
        if name is not None and pw is not None and em is not None:
            hashed_password = generate_password_hash(pw, method='sha256')
            
            new = Users(
                name=name, email=em, password=hashed_password,
                authenticated=False, validated=False, admin=False,
                n_scheduled_observations=0)
            users_db.session.add(new)
            print("Data inserted")
            users_db.session.commit()

            return [f"Account Created for {name}"]
        else:
            return ["Please fill out all fields"]
            # return [html.Div([html.H2('Already have a user account?'), dcc.Link('Click here to Log In', href='/login')])]


    @app.callback(Output("hidden_for_redirect", "children"), [Input("login-button", "n_clicks")],
                [State("email-box", "value"), State("pw-box", "value")])
    def login_success(n: int, email_value: str, pw_value: str) -> str:
        if n > 0:
            user = Users.query.filter_by(email=email_value).first()
            if user and check_password_hash(user.password, pw_value):
                #TODO check if "remember me box is checked"
                login_user(user)
                return dcc.Location(pathname="/", id="hi")
            else:
                pass
        else:
            pass
        
    
    @app.callback(Output("status-div", "children"), [Input("login-button", "n_clicks")],
                [State("email-box", "value"), State("pw-box", "value"),
                 State("login-button", "n_clicks")])
    def login_fail(_n, email_value, pw_value, n_clicks):
        if n_clicks > 0:
            user = Users.query.filter_by(email=email_value).first()
            if not user:
                return "account not found"
            elif not check_password_hash(user.password, pw_value):
                return "invalid password"
            else:
                pass
        else:
            pass
       

    # # TODO Move to separate layout or navbar
    # @app.callback(Output("url", "pathname"), [Input("logout-button", "n_clicks")])
    # def logout(n):
    #     # TODO
    #     """
    #     if n > 0:
    #         logout user (current user)
    #     else:
    #         pass
    #     """
    #     pass

    # TODO hide login fields, make back button
    @app.callback(Output("new-div", "children"), 
                  [Input("create-button", "n_clicks")],
                  [State("create-button", "n_clicks")])
    def create_fields(_n, n_clicks):
        if n_clicks > 0:
            create = html.Div([ html.H1("Create User Account")
            , dcc.Location(id="create_user", refresh=True)
            , dcc.Input(id="name"
                , type="text"
                , placeholder="name"
                , maxLength =15)
            , dcc.Input(id="email"
                , type="email"
                , placeholder="email"
                , maxLength = 50)
            , dcc.Input(id="password"
                , type="password"
                , placeholder="password")
            , html.Button("Create User", id="create-button", n_clicks=0)
            , html.Div(id="container-button-basic")
            ])

            return create
        else:
            pass
