import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

from pipeline import analyze

# ==========================================
# CYBERPUNK NASA STYLE
# ==========================================

BACKGROUND = "#050816"
CARD_BG = "rgba(20,30,60,0.55)"
CYAN = "#00F5FF"
GREEN = "#00FF9D"
ORANGE = "#FFB000"
RED = "#FF4D6D"
PURPLE = "#9D4EDD"


def card_style():

    return {
        "background": CARD_BG,
        "backdropFilter": "blur(14px)",
        "border": "2px solid rgba(0,245,255,0.25)",
        "boxShadow": "0 0 15px rgba(0,245,255,0.15)",
        "padding": "20px",
        "borderRadius": "18px",
        "flex": "1",
        "color": "white",
        "textAlign": "center"
    }


def big_text_style(color):

    return {
        "color": color,
        "fontSize": "42px",
        "fontWeight": "bold"
    }


# ==========================================
# FIGURES (rebuilt every time the slider moves)
# ==========================================

def make_gauge(title, value, bar_color):

    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#0000FF"},
                "bar": {"color": bar_color},
                "bgcolor": "rgba(20,30,60,0.55)"
            }
        )
    )


def make_figures(r):

    original = r["original"]

    wavelength = r["wavelength"]

    overlay_fig = go.Figure()

    overlay_fig.add_trace(
        go.Scatter(
            x=wavelength,
            y=original,
            name="Unknown Spectrum",
            line=dict(color=CYAN, width=3)
        )
    )

    overlay_fig.add_trace(
        go.Scatter(
            x=wavelength,
            y=r["reconstructed"],
            name="Reconstructed",
            line=dict(color=RED, width=3, dash="dash")
        )
    )

    overlay_fig.update_layout(
        template="plotly_dark",
        title="Spectral Comparison (Kubelka-Munk F(R) vs wavelength, um)",
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND
    )

    abundances = np.asarray(r["abundances"], dtype=float)

    plot_values = np.maximum(abundances, 1e-6)

    donut_fig = go.Figure(
        data=[
            go.Pie(
                labels=r["mineral_names"],
                values=plot_values.tolist(),
                customdata=(abundances * 100).tolist(),
                hovertemplate="%{label}: %{customdata:.1f}%<extra></extra>",
                textposition="inside",
                sort=False,
                hole=0.65
            )
        ]
    )

    donut_fig.update_layout(
        title="Mineral Composition",
        template="plotly_dark",
        paper_bgcolor=BACKGROUND
    )

    return {
        "overlay": overlay_fig,
        "donut": donut_fig,
        "conf": make_gauge(
            "Confidence",
            r["confidence"] * 100,
            "#39FF14"
        ),
        "unc": make_gauge(
            "Uncertainty",
            r["uncertainty"] * 100,
            "#FFB000"
        ),
        "anom": make_gauge(
            "Anomaly",
            min(r["anomaly"], 1.0) * 100,
            "#FF0000"
        ),
        "top_mineral": r["mineral_names"][
            int(np.argmax(r["abundances"]))
        ]
    }


# ==========================================
# MAIN DASHBOARD
# ==========================================

def build_dashboard(ctx):

    app = dash.Dash(__name__)


    # first render = no added noise
    r = analyze(ctx, 0.0)

    f = make_figures(r)

    # ======================================
    # MAP CARD (static)
    # ======================================

    map_df = pd.DataFrame({
        "Site": ["Analysis Site"],
        "Latitude": [24.5],
        "Longitude": [39.5]
    })

    map_fig = px.scatter_mapbox(
        map_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Site",
        zoom=4,
        height=350
    )

    map_fig.update_layout(
        mapbox_style="open-street-map",
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    # ======================================
    # SLIDER MARKS
    # ======================================

    marks = {}

    for i in range(11):

        v = round(i * 0.005, 3)

        marks[v] = {
            "label": str(v),
            "style": {
                "color": "#39FF14",
                "textShadow": "0 0 2px #39FF14"
            }
        }

    # ======================================
    # LAYOUT
    # ======================================

    app.layout = html.Div(
        style={
            "backgroundColor": BACKGROUND,
            "padding": "20px",
            "minHeight": "100vh",
            "fontFamily": "Arial"
        },
        children=[

            html.H1(
                "Planetary Reflectance Intelligent & Synergetic Mechanism ",
                style={"textAlign": "center", "color": CYAN}
            ),

            # ROW 1: map + noise slider
            html.Div([

                html.Div([
                    html.H3("Map"),
                    dcc.Graph(figure=map_fig)
                ], style=card_style()),

                html.Div([
                    html.H3(
                        "Noise Slider",
                        style={"color": "#FFFFFF"}
                    ),
                    dcc.Slider(
                        id="noise-slider",
                        min=0,
                        max=0.05,
                        step=0.005,
                        value=0,
                        marks=marks
                    )
                ], style=card_style())

            ], style={"display": "flex", "gap": "20px"}),

            html.Br(),

            # ROW 2: spectrum overlay
            html.Div([
                html.Div([
                    html.H3("Spectrum Overlay"),
                    dcc.Graph(id="overlay-graph", figure=f["overlay"])
                ], style=card_style())
            ]),

            html.Br(),

            # ROW 3: donut
            html.Div([
                html.Div([
                    html.H3("Donut Chart"),
                    dcc.Graph(id="donut-graph", figure=f["donut"])
                ], style=card_style())
            ], style={"display": "flex", "gap": "20px"}),

            html.Br(),

            # ROW 4: text cards
            html.Div([

                html.Div([
                    html.H4("Planetary Origin"),
                    html.H2(
                        r["planet"],
                        id="planet-text",
                        style=big_text_style("#696969")
                    )
                ], style=card_style()),

                html.Div([
                    html.H4("Predicted Mineral"),
                    html.H2(
                        r["label"],
                        id="mineral-text",
                        style=big_text_style("#FF4DFF")
                    )
                ], style=card_style()),

                html.Div([
                    html.H4("Top Mineral"),
                    html.H2(
                        f["top_mineral"],
                        id="top-text",
                        style=big_text_style("#B026FF")
                    )
                ], style=card_style()),

                html.Div([
                    html.H4("Geological Consistency"),
                    html.H5(
                        r["geo_message"],
                        id="geo-text",
                        style=big_text_style("#39FF14")
                    )
                ], style=card_style())

            ], style={"display": "flex", "gap": "20px"}),

            html.Br(),

            # ROW 5: gauges
            html.Div([

                html.Div([
                    dcc.Graph(id="conf-graph", figure=f["conf"])
                ], style=card_style()),

                html.Div([
                    dcc.Graph(id="unc-graph", figure=f["unc"])
                ], style=card_style()),

                html.Div([
                    dcc.Graph(id="anom-graph", figure=f["anom"])
                ], style=card_style())

            ], style={"display": "flex", "gap": "20px"})
        ]
    )

    # ======================================
    # SLIDER CALLBACK
    # ======================================

    @app.callback(
        Output("overlay-graph", "figure"),
        Output("donut-graph", "figure"),
        Output("planet-text", "children"),
        Output("mineral-text", "children"),
        Output("top-text", "children"),
        Output("geo-text", "children"),
        Output("conf-graph", "figure"),
        Output("unc-graph", "figure"),
        Output("anom-graph", "figure"),
        Input("noise-slider", "value")
    )
    def update_dashboard(noise):

        result = analyze(ctx, noise or 0.0)

        fig = make_figures(result)

        return (
            fig["overlay"],
            fig["donut"],
            result["planet"],
            result["label"],
            fig["top_mineral"],
            result["geo_message"],
            fig["conf"],
            fig["unc"],
            fig["anom"]
        )

    return app


def launch_dashboard(ctx):
    """Terminal use: build the dashboard and start a local server."""

    app = build_dashboard(ctx)

    app.run(debug=True)
