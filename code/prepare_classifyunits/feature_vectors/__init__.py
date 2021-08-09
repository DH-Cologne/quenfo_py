from . import convert_featurevectors


# from . import convert_featurevectors
# TODO: rückgabe später sollte kein string sein sondern ein vector
def get_featurevectors(cus: list):
    # TODO: FEATUREVECTOR

    # generate featurevector
    # listo = convert_featurevectors.get_vocab(cu.featureunits)
    # print(len(listo))

    fvs = 'filler'  # filler

    for cu in cus:
        cu.set_featurevectors(fvs)
