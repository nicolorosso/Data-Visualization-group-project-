import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

dash.register_page(__name__, name='Page 1')

# Assuming you have a DataFrame named df
# For demonstration purposes, I'm using a sample DataFrame
df = pd.read_csv("data/tweet_datavis.csv")
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

@callback(
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

    )

    return fig


most_active_users, most_mentioned_users = extract_insights(df)
insights_plot = create_insights_plot(most_active_users, most_mentioned_users)

layout=dbc.Container([

    # Eye-catching title
    dbc.Row([
        dbc.Col([
            html.H1('The 5th of January: Decoding Democracy Through Twitter',
                    style={'textAlign': 'center', "color" : "black", 'font-weight': 'bold'}),
            html.P("""What if we told you that the heartbeat of democracy could be traced in 280 characters or less? 
            From October 2020 to January 2021, we delved into the vibrant and volatile world of Twitter to dissect the discourse around #Trump. 
            Welcome to a digital exploration that uncovers the unexpected and confronts the unimaginable.""",
                   style={'textAlign': 'center', "color" :"black", 'font-size': '20px'})
        ], width=12)
    ]),

    # Visually striking image
    dbc.Row([
        dbc.Col([
            html.Img(src=r'assets/twitter_network.png', alt='image', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '80%'})
        ], width=12)
    ], align="center"),

    html.Div(style={'height':'30px'}),

    # Data Insights title
    dbc.Row([
        dbc.Col([
            html.H3('Insights from the Digital Battlefield', style={'textAlign': 'center', "color" : "black", 'font-weight': 'bold'}),
            html.P("Beyond the hashtags and retweets, Twitter holds a mirror to society. Our analysis reveals startling patterns and influential actors who steer the currents of conversation.")
        ], width=12)
    ]),

    # Data Insights
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=insights_plot),
            html.P("Step into the heart of the conversation with these key insights:", style={'textAlign': 'center', "color" :"black", 'font-size': '20px'}),
        ],width={'size':8, 'offset':2,'order':1}),
    ]),

    html.Div(style={'height':'30px'}),

    # Back to main page link
    dbc.Row([
        dbc.Col([
            dcc.Link('Venture Back to Main Page', href='/', style={'textAlign': 'center', 'display': 'block', 'color': 'blue'})
        ], width=12)
    ]),

    html.Div(style={'height':'30px'}),

    dbc.Row([
        dbc.Col([dcc.Input(id='dummy-input', type='hidden', value='dummy')], width=12)
    ])
])
