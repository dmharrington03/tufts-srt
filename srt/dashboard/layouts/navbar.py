"""navbar.py

Contains Functions for Interacting with a Navbar

"""

import dash_bootstrap_components as dbc

from flask_login import current_user

from ..messaging.user import User #<- how to import using path in Python?

try:
    from dash import html
except:
    import dash_html_components as html

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

def register_callbacks(app) -> None:
    """Registers the Callbacks for the Navbar
    Parameters
    ----------
    app : Dash Object
        Dash Object to Set Up Callbacks to
    Returns
    -------
    None
    """