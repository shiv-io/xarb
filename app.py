import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import os

import sqlalchemy as sa


postgres_conn_str = os.environ.get(
    "DATABASE_URL", "postgresql://admin:password@0.0.0.0:5432/admin"
)
# Heroku CLI returns DATABASE_URL with postgres:// but SQLAlchemy only supports postgresql://
if postgres_conn_str.startswith("postgres://"):
    postgres_conn_str = postgres_conn_str.replace("postgres://", "postgresql://", 1)
engine = sa.create_engine(postgres_conn_str)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Bitcoin Price Arbitrage Explorer",
)
server = app.server


def serve_layout():
    with engine.connect() as conn, conn.begin():
        cb = pd.read_sql(
            "SELECT base, currency, amount, created_at from cb_ticker", conn
        )
        wazir = pd.read_sql("SELECT at, sell from wazirx_ticker", conn).astype(
            {
                "sell": float,
            }
        )
        fx = pd.read_sql("SELECT last_updated_at, usd, inr from fx", conn)

    merged = pd.merge_asof(
        wazir,
        cb,
        left_on="at",
        right_on="created_at",
        allow_exact_matches=True,
        direction="nearest",
    )

    merged = pd.merge_asof(
        merged,
        fx,
        left_on="at",
        right_on="last_updated_at",
        allow_exact_matches=True,
        direction="nearest",
    )

    merged["spread"] = (merged["sell"] / merged["inr"]) - merged["amount"]
    merged["return_on_spread"] = merged["spread"] / merged["amount"]
    merged["sell_inr"] = merged["sell"] / merged["inr"]
    merged.sort_values(by=["at"], inplace=True)
    current_spread = merged["spread"].iloc[-1]

    # Return on spread
    fig = px.line(
        merged,
        x="at",
        y="return_on_spread",
        labels={"at": "Timestamp (UTC)"},
        title="Return on Spread",
    )
    fig.layout.yaxis.tickformat = ".2%"
    fig.update_layout(hovermode="x", yaxis_title="Return on Spread", height=600)
    fig.update_traces(mode="markers+lines", hovertemplate=None)

    # Spread (absolute value)
    layout = go.Layout(height=600)
    spread_fig = go.Figure(layout=layout)

    spread_fig.add_trace(
        go.Line(x=merged["at"], y=merged["amount"], name="Coinbase BTCUSD")
    )
    spread_fig.add_trace(
        go.Line(
            x=merged["at"],
            y=merged["sell_inr"],
            name="WazirX BTCUSD (converted from BTCINR)",
        )
    )
    spread_fig.update_layout(
        title="BTC Price Spread: Coinbase and WazirX",
        hovermode="x unified",
        xaxis_title="Timestamp (UTC)",
        yaxis_title="Price, USD",
        legend_title="",
        legend={"orientation": "h"},
        yaxis_tickformat="$",
    )
    spread_fig.update_traces(mode="markers+lines", hovertemplate="%{y}")
    return html.Div(
        children=[
            dbc.Row(
                [html.H1("Bitcoin Price Arbitrage Explorer")],
                justify="center",
                align="center",
            ),
            dbc.Row(
                [
                    html.Div(
                        children=f"""
                Monitor the spread in Bitcoin prices between Coinbase (large US-based crypto exchange)
                and WazirX (India-based crypto exchange). The current spread is ${round(current_spread, 2)}.
                """
                    )
                ],
                justify="center",
                align="center",
            ),
            dcc.Graph(id="spread", figure=spread_fig),
            dbc.Row(
                [
                    html.Div(
                        children=f"""
                The below chart shows a theoretical return on spread that can be achieved by buying low on one exchange
                and selling high on the other. Disclaimer: The data does not take into account fees and associated taxes.
                """
                    )
                ],
                justify="center",
                align="left",
            ),
            dcc.Graph(id="spread-return-pct", figure=fig),
        ]
    )


app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=True)
