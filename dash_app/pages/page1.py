import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


# Assuming you have a DataFrame named df
# For demonstration purposes, I'm using a sample DataFrame
df = pd.read_csv("tweet_datavis.csv")
# Extract the username and the id name from strquoted
df[['quoted_username', 'quoted_tweet_id']] = df['quoted_tweet'].str.extract(r'https:\/\/twitter\.com\/(\w+)\/status\/(\d+)')
# Extract the username from the mentions
df['mentioned_users'] = df['mentioned_users'].str.extract(r'https://twitter.com/(\w+)')

def extract_insights(df):
    # Number of tweets per user (the most active one)
    most_active_users = df['username'].value_counts().head(10)

    # Users with more mentions (more influential)
    mentioned_users = df['mentioned_users'].explode().dropna()
    most_mentioned_users = mentioned_users.value_counts().head(10)

    return most_active_users, most_mentioned_users

@app.callback(
    [Output(component_id='users_barplot', component_property='figure')],
    [Input(component_id='dummy-input', component_property='value')]
)

def update_output(dummy_value):
    # Top 5 Keywords Bar Plot
    users_barplot = insights_plot
    return users_barplot

def create_insights_plot(most_active_users, most_mentioned_users):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Most Active Users", "Most Mentioned Users"))

    fig.add_trace(
        go.Bar(x=most_active_users.index, y=most_active_users.values),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=most_mentioned_users.index, y=most_mentioned_users.values),
        row=1, col=2
    )

    fig.update_layout(
        showlegend=False,
        title="Twitter Insights",
    )

    return fig


most_active_users, most_mentioned_users = extract_insights(df)
insights_plot = create_insights_plot(most_active_users, most_mentioned_users)

layout = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.H1('The 5th of January: Dawn of a Democracy?', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.H3(),
            html.Img(src='assets/twitter_network.png', height="80%", width="80%", style={'textAlign': 'center'}), #app.get_asset_url('twitter_network.png')
            html.P("This is a graph representing the Community of Twitter around the #trump."),
        ], style={'width': '80%', 'display': 'inline-block','textAlign': 'center'}),

    ], style={'textAlign':'center'}),
    html.Br(),
    html.Div([
        html.H3('Data Insights'),
        html.P("This data was scraped from Twitter in the period between October 2020 and January 2021."),
        html.P("The following insights were extracted from the data:"),
        dcc.Graph(figure=insights_plot),
    ]),
    html.Br(),
    dcc.Link('Go back to the main page', href='/'),
    html.Div([dcc.Input(id='dummy-input', type='hidden', value='dummy')]),
], style={'textAlign':'center'})