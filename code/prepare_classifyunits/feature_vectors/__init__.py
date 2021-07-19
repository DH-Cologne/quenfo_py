
# from . import convert_featurevectors
# TODO: rückgabe später sollte kein string sein sondern ein vector
def get_featurevectors(cu):
    fvs = cu.featureunits

    # TODO: FEATUREVECTOR
    # generate featurevector (vorerst vllt mit tfidf)
    fvs = 'filler'    # filler
    cu.set_featurevectors(fvs)