import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash_bootstrap_templates import load_figure_template

load_figure_template("lumen")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

# Lendo os dados
df_data = pd.read_csv('supermarket_sales.csv')
df_data["Date"] = pd.to_datetime(df_data["Date"])
cidades = df_data["City"].value_counts().index

# ==================== Layout ======================== #
app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2("Meu negocio", style={"font-size": "20px"}),
                html.Hr(),
                html.H5("Produtos:", style={"font-size": "30px"}),
                dcc.Checklist(
                    options=[{"label": city, "value": city} for city in cidades],
                    value=cidades.tolist(), 
                    id="check_city", 
                    inputStyle={"margin-right": "5px", "margin-left": "20px"}
                ),
                html.P("Variável de análise:", style={"margin-top": "30px"}),
                dcc.RadioItems(
                    options=[
                        {"label": "Faturamento Bruto", "value": "gross income"},
                        {"label": "Avaliação", "value": "Rating"}
                    ], 
                    value="gross income", 
                    id="main_variable"
                ),
            ], style={"margin": "20px", "padding": "20px"})
        ], sm=2),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H3("Faturamento", style={"font-size": "20px"})
                    ], style={"height": "10vh", "margin": "20px", "padding": "10px"}, className="w-100"),
                ], sm=2, className="d-flex justify-content-center"),

                dbc.Col([
                    dbc.Card([
                        html.H3("Gastos", style={"font-size": "20px"})
                    ], style={"height": "10vh", "margin": "20px", "padding": "10px"}, className="w-100"),
                ], sm=2, className="d-flex justify-content-center"),

                dbc.Col([
                    dbc.Card([
                        html.H3("Lucro", style={"font-size": "20px"})
                    ], style={"height": "10vh", "margin": "20px", "padding": "10px"}, className="w-100"),
                ], sm=2, className="d-flex justify-content-center"),

                dbc.Col([
                    dbc.Card([
                        html.H3("N° Total de Vendas", style={"font-size": "20px"})
                    ], style={"height": "10vh", "margin": "20px", "padding": "10px"}, className="w-100"),
                ], sm=3, className="d-flex justify-content-center"),

                dbc.Col([
                    dbc.Card([
                        html.H3("Investimentos", style={"font-size": "20px"})
                    ], style={"height": "10vh", "margin": "20px", "padding": "10px"}, className="w-100"),
                ], sm=2, className="d-flex justify-content-center"),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="fig_totais")], sm=4)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="pay_fig")], sm=4)
            ]),
            dbc.Row([dcc.Graph(id="income_per_date_fig")]),
        ], sm=10)
    ])
])

# ===================== Callbacks =====================#
@app.callback([
            Output('fig_totais', 'figure'),
            Output('pay_fig', 'figure'),
            Output('income_per_date_fig', 'figure'),
        ],
            [
                Input('check_city', 'value'),
                Input('main_variable', 'value')
            ])
def render_graphs(cities, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]
    
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_income_time = df_filtered.groupby(["Date"])[main_variable].apply(operation).to_frame().reset_index()

    fig_totais = px.pie(df_city, values=main_variable, names="City", title="Total por Cidade")
    fig_payment = px.bar(df_payment, y="Payment", x=main_variable, orientation="h", title="Pagamentos")
    fig_income_date = px.bar(df_income_time, y=main_variable, x="Date", title="Faturamento ao longo do tempo")

    for fig in [fig_totais, fig_payment, fig_income_date]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=400, width=1200)
    
    return fig_totais, fig_payment, fig_income_date

# =============== Run server ===========================#
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8051, debug=True)
