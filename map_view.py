import plotly.express as px


def show_map():

    data = {

        "Name": ["Test Site"],

        "Lat": [24.5],

        "Lon": [39.5]

    }

    fig = px.scatter_mapbox(

        data,

        lat="Lat",

        lon="Lon",

        hover_name="Name",

        zoom=5

    )

    fig.update_layout(

        mapbox_style="open-street-map",

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )

    )

    fig.show()