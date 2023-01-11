from dash.dependencies import Input, Output, State
from dash import dcc
import base64
import pickle
import numpy as np
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from .sample_dataset import salary_raw
from .dash import Dash



country_raw = salary_raw["Country"].unique()
eduLevel_raw = salary_raw["EdLevel"].unique()
yearExp_raw = salary_raw["YearsCodePro"].unique()

predicted_model = pickle.load(open('app/dash/ml_model.pkl', 'rb'))
regressor_model = predicted_model["model"]
le_country = predicted_model["le_country"]
le_education = predicted_model["le_education"]


image_filename = 'app/static/developer.jpg'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

form = dbc.Card([
    html.Div(dbc.CardHeader("Machine learning model description"),
             className="mb-3 text-white"),
    dbc.Form(
        dbc.Col(
            [
                dbc.Label("Choose the country", html_for="dropdown"),
                dcc.Dropdown(
                    id="countryId",
                    options=[
                        {"label": cntry, "value": cntry} for cntry in country_raw
                    ],
                    className="mb-3",
                ),
                html.Br(),
                dbc.Label("Choose education Level", html_for="dropdown"),
                dcc.Dropdown(
                    id="eduLevelId",
                    options=[
                        {"label": edL, "value": edL} for edL in eduLevel_raw
                    ],
                    className="mb-4"
                ),
                html.Br(),
                dbc.Label("Year of experiance", html_for="slider"),
                dbc.Col(dcc.Slider(id="sliderId", min=0, max=30,
                                   step=1, value=3), className="mb-4"),

            ],
            className="g-2",
        )
    )], className="card w-55 me-4 needs-validation novalidate", color="light")

img_app = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
             width="500", height="300")
], className="img-card", style={
    'textAlign': 'center',
    'font-weight': 'bold'

})


button = html.Div(dbc.Button("Predict salary"), className="mt-4")
output_container = html.Div(className="mt-4 mb-4", style={
    'textAlign': 'center',

})

app_layout = dbc.Container([form, button, output_container, img_app])

def predict_salary(_, countrySelected, eduLevelSelected, yearExpSelected):
    XX = np.array([[countrySelected, eduLevelSelected, yearExpSelected]])
    XX[:, 0] = le_country.transform(XX[:, 0])
    XX[:, 1] = le_education.transform(XX[:, 1])
    XX = XX.astype(float)
    predicted_salary = regressor_model.predict(XX)
    return f"The average salary of developer with {yearExpSelected} years of experiences and  {eduLevelSelected}  background in {countrySelected}  is estimated to be {predicted_salary[0]:.3f}$." if countrySelected and eduLevelSelected else "No variables selected. Please choose the right variables !"



def init_callbacks(dash_app):
    dash_app.callback(
        # INPUT HERE
        Output(output_container, "children"),
        Input(button, "n_clicks"),
        State("countryId", "value"),
        State("eduLevelId", "value"),
        State("sliderId", "value"),
        prevent_initial_call=True,


    )(predict_salary)
    return dash_app


def init_dash(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server, routes_pathname_prefix="/predictive_model/", )

    # create dash layout
    dash_app.layout = app_layout

    # initialize callbacks
    init_callbacks(dash_app)

    return dash_app.server


if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    init_callbacks(app)
    app.run_server(debug=True, port=8080)
