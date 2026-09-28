def check_geological_consistency(
        abundances,
        mineral_names):

    abundance_dict = dict(
        zip(
            mineral_names,
            abundances
        )
    )

    quartz = abundance_dict.get(
        "Quartz",
        0
    )

    pyroxene = abundance_dict.get(
        "Pyroxene",
        0
    )

    if (

        quartz > 0.4

        and

        pyroxene > 0.4

    ):

        return (

            False,

            "Quartz and Pyroxene coexistence is uncommon"

        )

    return (

        True,

        "Geologically Consistent"

    )