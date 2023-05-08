import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import page1, page2, page3
from pages.navbar import header_menu, CONTENT_STYLE
# Add the 'dash-bootstrap-components' package to the import section
import dash_bootstrap_components as dbc

# App layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        header_menu,
        html.Div(id="page-content", className="container"),
    ]
)

index_layout = html.Div(
    [
        html.H1("TwitterPolitics", style={"textAlign": "center", "margin-top": "2rem"}),
        html.P(
            """
            In recent years, social media platforms like Twitter have played a significant role in politics.
            As a result, political conversations have become increasingly polarized, leading to a rise in
            disagreement and division among people with differing opinions. This app aims to provide insights
            into the impact of keywords on political discourse and the level of agreement/disagreement
            associated with them.
            """,
            className="lead",
            style={"marginTop": "40px", "fontSize": "20px", "textAlign": "justify", "textJustify": "inter-word"},
        ),
        html.Br(),
        html.H2('The structure of our analysis', style={'textAlign': 'center'}),
        html.Br(),
        html.Div([

            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('twitter_funnel copia.png'), height="100%", width="100%")
                    ]),
                    dbc.Col([
                        html.Br(),
                        html.H4("""We are going to focus on three levels of analysis:"""),
                        html.Br(),
                        html.H5("""Twitter Network:"""),
                        html.P("""The first level of our research focus on a general overview of the Twitter network over a period of 4 months: from October 2020, when the presidential debate started, till the 6th of January, the day after the Capitol Hill riot."""),
                        html.P("This first phase allowed us to gather some useful insights about the general debate on Twitter and some useful metrics, such as most active and most mentioned users."),
                        html.Br(),
                        html.H5("""Inter-Communities:"""),
                        html.P("""The second level of analysis focused on inter-communities relations. After finding the most common keywords, thanks to the greedy modularity community algorithm, we found communities of users among those keywords."""),
                        html.P("Our main purpose was to analyze the level of polarization of the political discourse between communities of users."),
                        html.Br(),
                        html.H5("""Intra-Communities:"""),
                        html.P("""The third level of analysis is among intra-communities relations. This third block aim to analyze the role of homophily in modeling members of the same communities. Is it true that member of similar communities tend to have similar level of agreements?""")
                    ])
                ])
            ])

                


            #html.Div(className="trend",children=[html.Ol(id='my-list', children=[html.Li(['first', 'second', 'third'])])],style={'textAlign': 'center'})
            ], style={'textAlign':'center'},),

            
        
        
                ], style=CONTENT_STYLE
)




# Update Page Container
@app.callback(
    Output(component_id="page-content", component_property="children"),
    [Input(component_id="url", component_property="pathname")],
)
def display_page(pathname):
    if pathname == "/page-1":
        return page1.layout
    elif pathname == "/page-2":
        return page2.layout
    elif pathname == "/page-3":
        return page3.layout
    else:
        return index_layout

