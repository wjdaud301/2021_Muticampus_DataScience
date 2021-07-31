import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('home', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Slider Graph'),
    dcc.Graph(id='graph-with-slider', animate=True, style={"backgroundColor":"#1a2d46", "color":"#ffffff"}),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500,paper_bgcolor="rgb(0,0,0,0)",plot_bgcolor="#1a2d46",
                        font = dict(color='white'))
    fig.update_xaxes(showgrid=True, gridcolor='#6d6d6d')
    fig.update_yaxes(showgrid=True, gridcolor='#6d6d6d')

    return fig
    
