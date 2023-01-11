from .dash import Dash
from dash import html
from dash import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
# Clean the data and extract some useful infromation
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


def load_data():
    salary_raw = pd.read_csv("app/data/survey_results_public.csv")
    salary_raw = salary_raw[["Country", "EdLevel", "YearsCodePro", "Age", "Gender",
                            "Employment", "ConvertedCompYearly"]]
    salary_raw = salary_raw[salary_raw["ConvertedCompYearly"].notnull()]
    salary_raw = salary_raw[salary_raw["Age"].notnull()]
    salary_raw = salary_raw.dropna()
    salary_raw = salary_raw[salary_raw["Employment"] == "Employed full-time"]
    salary_raw = salary_raw.drop("Employment", axis=1)

    country_map = shorten_categories(salary_raw.Country.value_counts(), 400)
    salary_raw["Country"] = salary_raw["Country"].map(country_map)
    salary_raw = salary_raw[salary_raw["ConvertedCompYearly"] <= 250000]
    salary_raw = salary_raw[salary_raw["ConvertedCompYearly"] >= 10000]
    salary_raw = salary_raw[salary_raw["Country"] != "Other"]

    salary_raw["YearsCodePro"] = salary_raw["YearsCodePro"].apply(
        clean_experience)
    salary_raw["EdLevel"] = salary_raw["EdLevel"].apply(clean_education)
    salary_raw = salary_raw.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return salary_raw


salary_raw = load_data()


# Getting first 50 raw to display as sample data 
df = salary_raw.head(50)

app_layout = html.Div(
    dash_table.DataTable(df.to_dict('records'), [
        {"name": i, "id": i} for i in df.columns], style_table={
        'maxHeight': '50ex',
        'overflowY': 'scroll',
        'width': '100%',
        'color': 'black',
        'minWidth': '100%',
        'background-color': 'black'
    }), className="container ")


def init_dash(server):
    dash_app = Dash(
        server=server, routes_pathname_prefix="/sample_dataset/",)
    dash_app.layout = app_layout
    return dash_app.server


if __name__ == "__main__":
    app = Dash(__name__)
    app.run_server(debug=True)
