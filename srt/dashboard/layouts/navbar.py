"""navbar.py

Contains Functions for Interacting with a Navbar

"""

import dash

try:
    from dash import dcc
except:
    import dash_core_components as dcc

import dash_bootstrap_components as dbc

from flask_login import current_user

from ..messaging.user import User #<- how to import using path in Python?

try:
    from dash import html
except:
    import dash_html_components as html

from dash.exceptions import PreventUpdate

from dash.dependencies import Input, Output, State

def generate_navbar(dropdowns, user, title="Commands"):
    """Generates the Navbar

    Parameters
    ----------
    dropdowns : dict
        Dictionary of Buttons for Each Dropdown Menu
    title : str
        Title of the Navbar

    Returns
    -------
    NavbarSimple
    """
    if user:

        navbar = dbc.NavbarSimple(
            [
                html.Div(
                    [
                        dbc.NavItem(f"Name: {user.name}"),
                        dbc.NavItem(f"Number of Observations: {user.n_scheduled_observations}")
                    ],
                    style={"display": "inline-block"}
                ),
                dbc.NavLink("Create Observation", id="btn-create-obs"),
                html.Div(
                    [
                        dbc.DropdownMenu(
                            children=dropdowns[drop_down],
                            in_navbar=True,
                            label=drop_down,
                            style={"display": "inline-block", "flexWrap": "wrap"},
                            className="m-1",
                        )
                        for drop_down in dropdowns
                    ]
                )
            ],
            brand=title,
            brand_style={"font-size": "large"},
            color="secondary",
            dark=True,
        )
        return navbar

# def generate_popups():
#     """Generates all 'Pop-up' Modal Components

#     Returns
#     -------
#     Div Containing all Modal Components
#     """

#     return dbc.Modal(
#         dbc.ModalHeader("Observation Information"),
#         id="obs-modal"
#     )

# def register_callbacks(app):
#     """Registers the Callbacks for the Navbar
#     Parameters
#     ----------
#     app : Dash Object
#         Dash Object to Set Up Callbacks to
#     Returns
#     -------
#     None
#     """

#     @app.callback(
#         Output("obs-modal", "is_open"),
#         [
#             Input("btn-create-obs", "n_clicks")
#             # Input("freq-btn-yes", "n_clicks"),
#             # Input("freq-btn-no", "n_clicks"),
#         ],
#         [
#             State("obs-modal", "is_open")
#             # State("frequency", "value"),
#         ],
#     )
#     def obs_click_func(n_clicks_btn, is_open): # FIGURE THIS OUT (BUTTON CALLBACK)
#         ctx = dash.callback_context
#         if not ctx.triggered:
#             return is_open
#         else:
#             # button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#             # if button_id == "freq-btn-yes":
#                 # command_thread.add_to_queue(f"freq {freq}")
#             if n_clicks_btn:
#                 return not is_open
#             return is_open
        
    # def obs_click_func(n_clicks_btn, n_clicks_yes, n_clicks_no, is_open): # FIGURE THIS OUT (BUTTON CALLBACK)
    #     ctx = dash.callback_context
    #     if not ctx.triggered:
    #         return is_open
    #     else:
    #         # button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    #         # if button_id == "freq-btn-yes":
    #             # command_thread.add_to_queue(f"freq {freq}")
    #         if n_clicks_yes or n_clicks_no or n_clicks_btn:
    #             return not is_open
    #         return is_open