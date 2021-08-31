set_5 = [1,3,5]
set_6 = [2,3,6]

def merge(reg, knn):
    if len(reg) == 1:
        if reg[0] == knn:
            return reg[0]
        else:
            return __if_subset([reg[0],knn], reg[0])
    elif len(reg) == 2:
        return __if_subset(reg, knn)
    else:
        return knn
    
def __if_subset(check:list, default):
    if set(check).issubset((set(set_5))):
        return 5
    elif set(check).issubset((set(set_6))):
        return 6
    else:
        return default