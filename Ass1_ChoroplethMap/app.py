# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv("Olympics_dataset.csv", skipinitialspace=True, thousands=",")

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Graph(id="medals_graph"),

    html.Div([
        html.H4("Games"),

        dcc.RadioItems(
            id="count_type",
            options=[
                {"label": "Combined Total", "value": "combined"},
                {"label": "Summer Games", "value": "summer"},
                {"label": "Winter Games", "value": "winter"}],
            value="combined"
        )],

        style={'width': '48%', 'display': 'inline-block'}
    ),

    html.Div([
        html.H4("Medals"),

        dcc.RadioItems(
            id="medal_type",
            options=[
                {"label": "All medals", "value": "all"},
                {"label": "Gold", "value": "gold"},
                {"label": "Silver", "value": "silver"},
                {"label": "Bronze", "value": "bronze"}
            ],
            value="all"
        )],

        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    )
])


@app.callback(
    dash.dependencies.Output("medals_graph", "figure"),
    [dash.dependencies.Input("count_type", "value"),
     dash.dependencies.Input("medal_type", "value")])
def update_figure(count_type, medal_type):
    if medal_type == "all":
        column_name = "Total_"
    elif medal_type == "gold":
        column_name = "Gold_"
    elif medal_type == "silver":
        column_name = "Silver_"
    else:
        column_name = "Bronze_"

    if count_type == "summer":
        column_name += "s"
    elif count_type == "winter":
        column_name += "w"
    else:
        column_name += "t"

    data = [dict(
        type="choropleth",
        locations=df["Country"],
        locationmode="country names",
        z=df[column_name],
        colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
                    [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
        autocolorscale=False,
        reversescale=True,
        marker=dict(
            line=dict(
                color="rgb(180,180,180)",
                width=0.5
            )),
        colorbar=dict(
            autotick=False,
            title="Number of medals"),
    )]

    layout = dict(
        title="All-time Olympic Games medal",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection=dict(
                type="Mercator"
            )
        )
    )

    return {"data": data, "layout": layout}


if __name__ == "__main__":
    app.run_server(debug=True)
