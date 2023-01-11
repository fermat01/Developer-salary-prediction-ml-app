"""
Dash port of Shiny iris k-means example:

https://shiny.rstudio.com/gallery/kmeans-example.html
"""
import dash_bootstrap_components as dbc
from dash import dcc
import dash
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from sklearn import datasets
from sklearn.cluster import KMeans
from .dash import Dash
import plotly.express as px
from .sample_dataset import salary_raw

from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)
df_data = salary_raw.to_dict()
'''
df_data = pd.read_json("app/data/test.json")'''

app_layout = html.Div(
    [
        html.P("Choose the first raw column (x-axis):"),
        dcc.Dropdown(
            id="x_axis",
            options=[{"value": x, "label": x} for x in df_data.keys()],
            clearable=False,
            style={"width": "40%", "color": "black"},
    ),
        html.P("Choose the second raw column (y-axis):"),
        dcc.Dropdown(
            id="y_axis",
            options=[{"value": y, "label": y} for y in df_data.keys()],
            clearable=False,
            style={"width": "40%", "color": "black"},
    ),

        html.P("Choose a graph to display:"),
        dcc.Dropdown(
            id="graph",
            options=[
                {"value": "pie", "label": "Pie chart"},
                {"value": "line", "label": "Line chart"},
                {"value": "bar", "label": "Bar chart"},
                {"value": "box", "label": "Boxplot chart"},
                {"value": "scatter", "label": "Scatter chart"},
                {"value": "2dhistogram", "label": "2d-histogram chart"},
            ],
            clearable=False,
            style={"width": "40%"},
            className=" mb-5 "
            # multi=True
    ),
        dcc.Graph(id="my_graph", figure={}),
    ], className="container "
)


def generate_chart(x_axis, y_axis, graph):
    if not x_axis:
        raise PreventUpdate
    if not y_axis:
        raise PreventUpdate
    if not graph:
        raise PreventUpdate
    dff = df_data
    if graph == "pie":
        fig = px.pie(dff, values=y_axis, names=x_axis, title="Pie Chart")
    elif graph == "line":
        fig = px.line(dff, x=x_axis, y=y_axis, title="Line Chart")
    elif graph == "bar":
        fig = px.bar(dff, x=x_axis, y=y_axis, title="Bar Chart")
    elif graph == "box":
        fig = px.box(dff, x=x_axis, y=y_axis, title="Boxplot Chart")
    elif graph == "boxplot":
        fig = px.scatter(dff, x=x_axis, y=y_axis, title="Scatter Chart")
    elif graph == "2dhistogram":
        fig = px.density_heatmap(
            dff,
            x=x_axis,
            y=y_axis,
            nbinsx=20,
            nbinsy=20,
            color_continuous_scale="Viridis",
            title="2D Histogram Chart",
        )
    else:
        fig = px.pie(dff, values=y_axis, names=x_axis, title="Pie Chart")

    return fig


def init_callbacks(dash_app):
    dash_app.callback(
        Output("my_graph", "figure"),
        [
            Input("x_axis", "value"),
            Input("y_axis", "value"),
            Input("graph", "value"),
        ],
        
    )(generate_chart)


def init_dash(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server, routes_pathname_prefix="/data_exploration/", )

    # create dash layout
    dash_app.layout = app_layout
    # initialize callbacks
    init_callbacks(dash_app)

    return dash_app.server


if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.run_server(debug=True, port=8080)
