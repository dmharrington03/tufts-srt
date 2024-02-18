"""data_page.py

Function for Generating Data Page and Creating Callbacks

"""

try:
    from dash import dcc
except:
    import dash_core_components as dcc

try:
    from dash import html
except:
    import dash_html_components as html

from dash.dependencies import Input, Output, State

from urllib.parse import quote as urlquote
from datetime import datetime
from pathlib import Path


def generate_layout(user):
    """Generates the Basic Layout for the Data Page

    Returns
    -------
    Data Page Layout
    """
    layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "My Data",
                                style={"text-align": "center"},
                            ),
                            html.Div(
                                "No Observation data yet",
                                style={
                                    "height": 200,
                                    "overflow": "hidden",
                                    "overflow-y": "scroll",
                                },
                            ),
                        ],
                        className="pretty_container twelve columns",
                    ),
                ],
                className="flex-display",
                style={"justify-content": "center", "margin": "5px"},
            ),
        ]
    )
    return layout


def register_callbacks(app, config, status_thread):
    """Registers the Callbacks for the System Page

    Parameters
    ----------
    app : Dash Object
        Dash Object to Set Up Callbacks to
    config : dict
        Contains All Settings for Dashboard / Daemon
    status_thread : Thread
        Thread for Getting Status from Daemon

    Returns
    -------
    None
    """

    pass