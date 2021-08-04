listo = list()

def get_vocab(fus):
    global listo
    for fu in fus:
        listo.append(fu)
    listo = sorted(list(dict.fromkeys(listo)))
    return listo
