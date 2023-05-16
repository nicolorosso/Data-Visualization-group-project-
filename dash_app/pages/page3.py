import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import numpy as np
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Page 2')


with open("data/edge_betweenness_dataframes.json", 'r') as infile:
    loaded_json_data = json.load(infile)

# Convert the JSON objects to dataframes
result_dfs_edge_betweenness = {}

for kw, json_obj in loaded_json_data.items():
    result_dfs_edge_betweenness[kw] = pd.read_json(json_obj, orient='records')

image_path = 'assets/twitter_network.png'

faq_section = html.Div([
    dbc.Button("FAQ", id="faq_toggle", className="mb-3"),
    dbc.Collapse([
        dbc.Card([
            dbc.CardHeader("1. Identify the most common keywords related to the political discourse."),
            dbc.CardBody(
                "In this analysis, we first identify the top 7 keywords that are most frequently mentioned in the collected Twitter data. This helps to narrow down the focus of our analysis on the most relevant topics in the political discourse."),
        ]),
        dbc.Card([
            dbc.CardHeader("2. Use the greedy modularity algorithm to find communities for each keyword."),
            dbc.CardBody(
                "We then use the greedy modularity algorithm to identify communities for each keyword. This algorithm is a popular method for detecting communities in networks, allowing us to group users that are closely related in the context of the keyword."),
        ]),
        dbc.Card([
            dbc.CardHeader("3. Compute the level of agreement within each community using the RoBERTa-large algorithm."),
            dbc.CardBody(
                "Next, we compute the level of agreement within each community using the RoBERTa-large algorithm, which is a state-of-the-art natural language processing model. By analyzing the sentiment and content of the tweets, this algorithm allows us to understand the degree of agreement among users within each community."),
        ]),
        dbc.Card([
            dbc.CardHeader("4. Visualize the level of polarization within communities using the Kruskal-Wallis test."),
            dbc.CardBody(
                "Finally, we visualize the level of polarization within communities using the Kruskal-Wallis test. This statistical test helps us compare the distributions of edge betweenness within communities, allowing us to observe how polarized the communities are based on the selected keywords."),
        ]),
    ], id="faq_collapse"),
])



layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Unveiling Polarization: A Twitter Discourse Analysis',
                    style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'black'}),
            html.P("""Journey with us as we delve into the Twitterverse, harnessing the power of keywords to unravel political discourse.
            Our exploration reveals not only the most tweeted keywords, but also the polarization within communities. This unique insight allows us 
            to gauge the state of political discourse with unparalleled depth.
            """,
                    style={'textAlign': 'center', 'color': 'black','font-size': '20px'})

        ], width=12)
    ], style={'marginBottom': '50px', 'marginTop': '50px'}),

    dbc.Row([
        dbc.Col([
            html.H4("Top 7 Keywords by Occurrence: The Power Players of Political Discourse",
                    style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'black'}),
            dcc.Graph(id="keywords_barplot"),
        ], width=6),
        dbc.Col([
            html.H4("Edge Betweenness Percentiles: Unveiling the Bridge Keywords",
                    style={'textAlign': 'center', 'font-weight': 'bold', 'color': 'black'}),
            dcc.Graph(id="edge_bet_percentiles_plot"),
        ], width=6),
    ], style={'marginBottom': '50px'}),

    dbc.Row([
        dbc.Col([
            html.H4("How We Did It: A Peek Behind The Curtain",
                    style={'textAlign': 'left', 'font-weight': 'bold', 'color': 'black'}),
            faq_section,
        ], width=12)
    ], style={'marginBottom': '30px', 'marginTop': '30px'}),

    dbc.Row([
        dbc.Col([
            dcc.Link('Want more? Return to the main page', href='/')
        ], width=12, style={'textAlign': 'center', 'marginBottom': '30px', 'marginTop': '30px'}),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Input(id='dummy-input', type='hidden', value='dummy')
        ], width=12)
    ])
])

@callback(
    [Output(component_id='keywords_barplot', component_property='figure'),
     Output(component_id='edge_bet_percentiles_plot', component_property='figure')],
    [Input(component_id='dummy-input', component_property='value')]
)

def update_output(dummy_value):
    # Top 5 Keywords Bar Plot
    keywords_barplot = create_top_7_keywords_barplot()

    # Edge Betweenness Percentiles Plot
    edge_bet_percentiles_plot = create_edge_bet_percentiles_plot()

    return keywords_barplot, edge_bet_percentiles_plot


def create_top_7_keywords_barplot():
    # Get the top 7 keywords by the number of occurrences in the result_dfs_edge_betweenness
    top_keywords = sorted(result_dfs_edge_betweenness.keys(), key=lambda x: len(result_dfs_edge_betweenness[x]), reverse=True)[:7]
    top_occurrences = [len(result_dfs_edge_betweenness[keyword]) for keyword in top_keywords]

    # Create the bar plot
    fig = go.Figure(go.Bar(x=top_keywords, y=top_occurrences))
    fig.update_layout(
                      xaxis_title='Keywords',
                      yaxis_title='Occurrences')
    return fig



def create_edge_bet_percentiles_plot():
    percs = np.linspace(80, 100, 500)
    fig = go.Figure()

    for idx, (keyword, df) in enumerate(result_dfs_edge_betweenness.items()):
        edges_agreement = df.loc[df.agreement == 1].edge_bet.values
        edges_disagreement = df.loc[df.agreement == -1].edge_bet.values

        qn_edges_agreement = np.percentile(edges_agreement, percs)
        qn_edges_disagreement = np.percentile(edges_disagreement, percs)

        fig.add_trace(
            go.Scatter(x=percs[450:], y=qn_edges_agreement[450:], name=f"{keyword} Agreement",
                       visible=True if idx == 0 else "legendonly")
        )

        fig.add_trace(
            go.Scatter(x=percs[450:], y=qn_edges_disagreement[450:], name=f"{keyword} Disagreement",
                       visible=True if idx == 0 else "legendonly")
        )

    dropdown_buttons = [
        dict(
            args=[{"visible": [True if trace_idx in [2 * idx, 2 * idx + 1] else False
                               for trace_idx in range(2 * len(result_dfs_edge_betweenness))]}],
            label=keyword,
            method="update"
        ) for idx, keyword in enumerate(result_dfs_edge_betweenness)
    ]

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, showactive=True)],

        xaxis_title="Percentiles",
        yaxis_title="Edge Betweenness",
        yaxis_type="log",
        legend_title="Keywords",
        hovermode="x"
    )

    return fig

@callback(
    Output("faq_collapse", "is_open"),
    [Input("faq_toggle", "n_clicks")],
    [State("faq_collapse", "is_open")],
)
def toggle_faq(n, is_open):
    if n:
        return not is_open
    return is_open
