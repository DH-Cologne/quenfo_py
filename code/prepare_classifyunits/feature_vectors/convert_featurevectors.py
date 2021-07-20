listo = list()
# packe die ngramme der fus in eine liste um ein unique vocab zu erhalten
# noch kommen hier rund 20.000 raus, bei java rund 10.000 ngramme/features warum?
def get_vocab(fus):
    global listo
    for fu in fus:
        listo.append(fu)
    listo = sorted(list(dict.fromkeys(listo)))
    return listo