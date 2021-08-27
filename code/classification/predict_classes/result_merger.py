def merge(reg, knn):

    # prepare regex prediction (eigene funktion)
    ids = list()
    for i in reg:
        ids.append(int(i[0]))
    ids = list(dict.fromkeys(ids))

    # check if more than one match in regex
    if len(ids) > 1:
        if 1 in ids and 3 in ids and len(ids) == 2:
            reg = 5
        elif 2 in ids and 3 in ids and len(ids) == 2:
            reg = 6
        else:
            # mehr als 2 klassen wurden gefunden, irgendwas ist schiefgelaufen, nimm lieber knn
            reg = knn
    else:
        reg = int(ids[0])

    # zweite funktion
    # vergleich mit knn
    if reg == knn:
        predicted = reg
        return predicted
    else:
        if (reg == 1 and knn ==3) or (reg == 3 and knn ==1):
            predicted = 5
        elif (reg == 2 and knn ==3) or (reg == 3 and knn ==2):
            predicted = 6
        elif (reg == 5 and knn ==1) or (reg == 5 and knn == 3) or (reg == 1 and knn ==5) or (reg == 3 and knn == 5):
            predicted = 5
        elif (reg == 6 and knn ==2) or (reg == 6 and knn == 3) or (reg == 2 and knn ==6) or (reg == 3 and knn == 56):
            predicted = 6
        else:
            predicted = reg
            #predicted = knn
    return predicted