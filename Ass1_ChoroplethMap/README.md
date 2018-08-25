# Choropleth Map of Olympics Medals

In this activity, we will use the [Plotly](https://plot.ly/) library to create an 
interactive choropleth map of Olympics medals. We will then make use of the 
[Dash](https://plot.ly/products/dash/) library to create a very simple web app to 
display the map.

## Getting Started

Install the required packages using the following command

```
pip install -r requirements.txt
```

## Creating an interactive choropleth map

Here we use the Olympics dataset that has already been tidied up. 
We generally pass in two arguments into the plotly plot function

* `data` is used to pass in the data to be plotted
* `layout` is used to customise the layout such as setting the title and font

```python
import pandas as pd
import plotly.offline as py

df = pd.read_csv("Olympics_dataset.csv", thousands=",")

data = [dict(
    type="choropleth",
    locations=df["Country"],
    locationmode="country names",
    z=df["Total_t"],
    colorbar=dict(title="Number of medals")
)]

layout = dict(
    title="All-time Olympic Games medal"
)

fig = dict(data=data, layout=layout)
py.plot(fig, filename='cloropleth_map.html')
```

### Customising the choropleth map

We can change the colour scale by passing in a list of colour scales

```python
data = [dict(
    type="choropleth",
    locations=df["Country"],
    locationmode="country names",
    z=df["Total_t"],
    colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
                [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
    autocolorscale=False,
    reversescale=True,
)]
```

You can look for more customisation on the [reference page](https://plot.ly/python/reference/#choropleth) for choropleth maps

## Creating a simple web app

Using the `data` and `layout` variables from above, we can create a very basic web app with a few lines of code. 
Create a file named `app.py` with the following code

```python
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(
        id="medals_graph",
        figure={
            "data": data,
            "layout": layout
        }
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

Run it with `python app.py` and visit [http:127.0.0.1:8050/](http:127.0.0.1:8050/) in your web browser.
You should be able to see your app

### Adding a basic callback function

Let's add some radio buttons to show the medals in different Olympics games using `RadioItems`.
Create a new file or replace `app.py` as follow

```python
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv("Olympics_dataset.csv", skipinitialspace=True, thousands=",")

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="medals_graph"),

    html.Div([
        html.H4("Games"),

        dcc.RadioItems(
            id="game_type",
            options=[
                {"label": "Combined Total", "value": "combined"},
                {"label": "Summer Games", "value": "summer"},
                {"label": "Winter Games", "value": "winter"}],
            value="combined"
        )]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

And we need to create a callback function to handle the input from the radio buttons. 
We set the column name based on the radio button input to extract the relevant data from the dataframe.

```python
@app.callback(
    dash.dependencies.Output("medals_graph", "figure"),
    [dash.dependencies.Input("game_type", "value")])
def update_figure(game_type):
    if game_type == "summer":
        column_name = "Total_s"
    elif game_type == "winter":
        column_name = "Total_w"
    else:
        column_name = "Total_t"

    data = [dict(
        type="choropleth",
        locations=df["Country"],
        locationmode="country names",
        z=df[column_name],
        colorbar=dict(title="Number of medals")
    )]

    layout = dict(
        title="All-time Olympic Games medal"
    )

    return {"data": data, "layout": layout}
```

### Challenge

Add another set of radio buttons of medal types to choose from. 
[Here](https://comp9321-ass1-extra.herokuapp.com/) is an example of the final web app.

## References

* https://plot.ly/python/choropleth-maps/
* https://dash.plot.ly/getting-started-part-2