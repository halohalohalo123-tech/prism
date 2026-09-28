import dash
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd


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

        "boxShadow":
        "0 0 15px rgba(0,245,255,0.15)",

        "padding": "20px",

        "borderRadius": "18px",

        "flex": "1",

        "color": "white",

        "textAlign": "center"
    }


# ==========================================
# MAIN DASHBOARD
# ==========================================

def launch_dashboard(

        mineral,

        confidence,

        uncertainty,

        anomaly,

        abundances,

        mineral_names,

        original,

        reconstructed,

        planet,

        geo_message

):

    app = dash.Dash(__name__)

    # ======================================
    # MAP CARD
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

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    # ======================================
    # OVERLAY SPECTRUM
    # ======================================

    wavelength = np.linspace(

        0.35,

        2.5,

        len(original)

    )

    overlay_fig = go.Figure()

    overlay_fig.add_trace(

        go.Scatter(

            x=wavelength,

            y=original,

            name="Unknown Spectrum",

            line=dict(

                color=CYAN,

                width=3
            )
        )
    )

    overlay_fig.add_trace(

        go.Scatter(

            x=wavelength,

            y=reconstructed,

            name="Reconstructed",

            line=dict(

                color=RED,

                width=3,

                dash="dash"
            )
        )
    )

    overlay_fig.update_layout(

        template="plotly_dark",

        title="Spectral Comparison",

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND
    )

    # ======================================
    # DONUT
    # ======================================

    donut_fig = go.Figure(

        data=[

            go.Pie(

                labels=mineral_names,

                values=abundances,

                hole=0.65
            )

        ]

    )

    donut_fig.update_layout(

        title="Mineral Composition",

        template="plotly_dark",

        paper_bgcolor=BACKGROUND
    )

    # ======================================
    # BAR CHART
    # ======================================

    abundance_fig = go.Figure(

        data=[

            go.Bar(

                x=mineral_names,

                y=abundances * 100
            )

        ]

    )

    abundance_fig.update_layout(

        title="Mineral Abundances",

        template="plotly_dark",

        paper_bgcolor=BACKGROUND
    )

    # ======================================
    # TOP MINERAL
    # ======================================

    top_idx = np.argmax(abundances)

    top_mineral = mineral_names[top_idx]

    # ======================================
    # GAUGES
    # ======================================

    conf_gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=confidence * 100,

            title={"text": "Confidence"},

            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#0000FF'},
                'bar': {'color': '#39FF14'},
                'bgcolor': 'rgba(20,30,60,0.55)'
            }
        )
    )

    unc_gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=uncertainty * 100,

            title={"text": "Uncertainty"},

            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#0000FF'},
                'bar': {'color': '#FFB000'},
                'bgcolor': 'rgba(20,30,60,0.55)'
            }
        )
    )

    anom_gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=min(anomaly, 100),

            title={"text": "Anomaly"},

            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#0000FF'},
                'bar': {'color': '#FF0000'},
                'bgcolor': 'rgba(20,30,60,0.55)'
            }
        )
    )

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

                "COGNITIVE CROSS-PLANETARY SPECTRAL PERCEIVER ",

                style={

                    "textAlign": "center",

                    "color": CYAN
                }
            ),

            # ==================================
            # ROW 1
            # ==================================

            html.Div([

                html.Div([

                    html.H3("Map"),

                    dcc.Graph(
                        figure=map_fig
                    )

                ], style=card_style()),

                html.Div([

                    html.H3(
                        "Noise Slider",
                        style={
                            "color": "#FFFFFF"
                        }
                    ),

                    dcc.Slider(
                        id="noise-slider",

                        min=0,

                        max=0.05,

                        step=0.005,

                        value=0.005,

                        marks={

                            0: {
                                "label": "0",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.005: {
                                "label": "0.005",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.01: {
                                "label": "0.01",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.015: {
                                "label": "0.015",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.02: {
                                "label": "0.02",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.025: {
                                "label": "0.025",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.03: {
                                "label": "0.03",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.035: {
                                "label": "0.035",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.04: {
                                "label": "0.04",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.045: {
                                "label": "0.045",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            },

                            0.05: {
                                "label": "0.05",
                                "style": {
                                    "color": "#39FF14",
                                    "textShadow": "0 0 2px #39FF14"
                                }
                            }
                        }
                    )

                ], style=card_style())

            ],

            style={

                "display": "flex",

                "gap": "20px"
            }),

            html.Br(),

            # ==================================
            # ROW 2
            # ==================================

            html.Div([

                html.Div([

                    html.H3(
                        "Spectrum Overlay"
                    ),

                    dcc.Graph(
                        figure=overlay_fig
                    )

                ], style=card_style())

            ]),

            html.Br(),

            # ==================================
            # ROW 3
            # ==================================

            html.Div([

                html.Div([

                    html.H3(
                        "Donut Chart"
                    ),

                    dcc.Graph(
                        figure=donut_fig
                    )

                ], style=card_style())

            ],

            style={

                "display": "flex",

                "gap": "20px"
            }),

            html.Br(),

            # ==================================
            # ROW 4
            # ==================================

            html.Div([

                html.Div([

                    html.H4(
                        "Planetary Origin"
                    ),

                    html.H2(planet, 
                    style={
                        "color": "#696969",
                        "fontSize": "42px",
                        "fontWeight":"bold"
                    }
                    )

                ], style=card_style()),

                html.Div([

                    html.H4(
                        "Predicted Mineral"
                    ),

                    html.H2(mineral,
                    style={
                        "color":"#FF4DFF",
                        "fontSize":"42px",
                        "fontWeight":"bold"
                    }
                    )

                ], style=card_style()),

                html.Div([

                    html.H4(
                        "Top Mineral"
                    ),

                    html.H2(top_mineral,
                    style={
                        "color": "#B026FF",
                        "fontSize": "42px",
                        "fontWeight": "bold"
                    }
                    )

                ], style=card_style()),

                html.Div([

                    html.H4(
                        "Geological Consistency"
                    ),

                    html.H5(
                        geo_message,
                        style={
                            "color":"#39FF14",
                            "fontSize":"42px" ,
                            "fontWeight":"bold"
                        }
                    )

                ], style=card_style())

            ],

            style={

                "display": "flex",


"gap": "20px"
            }),

            html.Br(),


            # ==================================
            # ROW 6
            # ==================================

            html.Div([

                html.Div([

                    dcc.Graph(

                        figure=conf_gauge

                    )

                ], style=card_style()),

                html.Div([

                    dcc.Graph(

                        figure=unc_gauge

                    )

                ], style=card_style()),

                html.Div([

                    dcc.Graph(

                        figure=anom_gauge

                    )

                ], style=card_style())

            ],

            style={

                "display": "flex",

                "gap": "20px"
            })

        ]
    )

    app.run(debug=True)

