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
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('twitter_funnel copia.png'), height="30%", width="30%"),
                html.P("""
                We are going to focus on three levels of analysis: 
                - 
                """),
            ], style={'width': '80%', 'display': 'inline-block', 'textAlign': 'center'}),
        ]),
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

