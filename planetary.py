def detect_planetary_origin(
        abundances,
        mineral_names):

    abundance_dict = dict(
        zip(
            mineral_names,
            abundances
        )
    )

    earth_score = (

        abundance_dict.get(
            "Quartz",
            0
        )

        +

        abundance_dict.get(
            "Kaolinite",
            0
        )

        +

        abundance_dict.get(
            "Basalt",
            0
        )

    )

    moon_score = (

        abundance_dict.get(
            "Pyroxene",
            0
        )

        +

        abundance_dict.get(
            "Anorthite",
            0
        )

    )

    mars_score = (

        abundance_dict.get(
            "Hematite",
            0
        )

        +

        abundance_dict.get(
            "Jarosite",
            0
        )

    )

    scores = {

        "Earth": earth_score,

        "Moon": moon_score,

        "Mars": mars_score

    }

    planet = max(
        scores,
        key=scores.get
    )

    return planet