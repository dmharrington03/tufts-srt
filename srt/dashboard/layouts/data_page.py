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
from ..messaging.observation import Observation

    
def generate_layout(user):
    """Generates the Basic Layout for the Data Page

    Returns
    -------
    Data Page Layout
    """

    obs_table = html.Div("No Observation Data")

    if (user != None and len(user.observations) > 0):
        # completed = [ obs for obs in user.observations ]
        obs = user.observations[0]
        obs_data = obs.get_display_data()

        table_data = []

        for obs in user.observations:
            obs_data = obs.get_display_data()
            table_data.append(
                html.Tr([ html.Td(obs_data.get(i)) for i in obs_data.keys() ])
            )

        obs_table = html.Table(
            [ html.Tr([ html.Th(col, style={"fontWeight": "900"}) for col in obs_data.keys()]) ] +
            table_data
        )


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
                                obs_table,
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