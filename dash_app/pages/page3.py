import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from app import app  # Import app from app.py
import plotly.graph_objs as go
import pandas as pd
import json
import networkx as nx
import plotly.express as px


with open(r"C:\Users\nickr\Downloads\edge_betweenness_dataframes.json", 'r') as infile:
    loaded_json_data = json.load(infile)

# Convert the JSON objects to dataframes
result_dfs_edge_betweenness = {}

for kw, json_obj in loaded_json_data.items():
    result_dfs_edge_betweenness[kw] = pd.read_json(json_obj, orient='records')

# Define the app layout
import dash_core_components as dcc

layout = html.Div([
    html.Div([
        html.P(
            """
            This interactive network graph shows the relationships between different communities discussing the selected keyword.
            The graph is based on the edge betweenness of the communities. Use the dropdown menu to select a keyword and explore the network graph.
            """,
            style={"textAlign": "justify", "margin": "20px"},
        ),
    ]),
    dcc.Graph(id='network-graph'),
    dcc.Dropdown(
        id='keyword-dropdown',
        options=[{"label": kw, "value": i} for i, kw in enumerate(result_dfs_edge_betweenness.keys())],
        value=0,
        clearable=False,
        style={"width": "50%", "margin": "0 auto"},
    ),
])


def create_network_graph(keyword, df):
    # Group the data by SourceModularity and TargetModularity
    grouped = df.groupby(['SourceModularity', 'TargetModularity'])

    # Filter out self-looping communities
    filtered_groups = [(name, group) for name, group in grouped if name[0] != name[1]]

    # Create a NetworkX graph from the filtered DataFrame
    G = nx.from_pandas_edgelist(pd.concat([group for _, group in filtered_groups]), 'SourceModularity',
                                'TargetModularity', edge_attr=True, create_using=nx.DiGraph())

    # Get node positions using a layout algorithm (you can use other layout algorithms as well)
    pos = nx.spring_layout(G, seed=42)

    # Get a list of colors
    colors = px.colors.qualitative.Plotly

    # Create node trace
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes],
        y=[pos[node][1] for node in G.nodes],
        text=[str(node) for node in G.nodes],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            color=[colors[int(node) % len(colors)] for node in G.nodes],
            size=15,
            line_width=2
        )
    )

    # Create edge trace
    edge_trace = go.Scatter(
        x=[pos[edge[0]][0] for edge in G.edges] + [pos[edge[1]][0] for edge in G.edges],
        y=[pos[edge[0]][1] for edge in G.edges] + [pos[edge[1]][1] for edge in G.edges],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Create a Plotly figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'Network Graph for Keyword "{keyword}"',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    return fig

# Define the callback for updating the network graph
@app.callback(
    Output('network-graph', 'figure'),
    Input('keyword-dropdown', 'value')
)
def update_graph(selected_keyword_index):
    # Get the selected keyword and DataFrame
    keyword, df = list(result_dfs_edge_betweenness.items())[selected_keyword_index]

    # Create the network graph for the selected keyword
    figure = create_network_graph(keyword, df)

    return figure
