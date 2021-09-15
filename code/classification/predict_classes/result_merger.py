""" Script contains the result_merger step. Both predictions (knn and reg) for one cu are compared. """

# Define Variables -> a paragraph can contain different class-elements (e.g. 1 and 3)
# --> class 5 is set if paragraph gets sorted in classes 1 and 3 (or 5)
# --> class 6 is set if paragraph gets sorted in classes 2 and 4 (or 6)
set_5 = [1,3,5]
set_6 = [2,3,6]

# ## Functions
def merge(reg: list, knn: int) -> int:
    """ Function to compare and merge the predictions of knn and reg.
    
    Parameters
    ----------
    reg: list
        The predicted class(es) from regex_classifier.
    knn: int
        The predicted class from knn_classifier.
        
    Returns
    -------
    predicted:  int
        Final predicted class for a cu. """
        
    # Does reg-list contain more than one element?
    # If only 1, compare it with the knn-prediction
    if len(reg) == 1:
        # Both are equal, set prediction as final choice.
        if reg[0] == knn:
            return reg[0]
        # Both are not equal, check if they are part of one of the subsets (set_5 or set_6), else use regex prediction as default.
        else:
            return __if_subset([reg[0],knn], reg[0])
    # Two predictions in reg-list?
    elif len(reg) == 2:
        # Check if they are part of the subsets (set_5 or set_6), else regex prediction is not usable --> set knn prediction as default.
        return __if_subset(reg, knn)
    # More than to prediction in reg-list? --> unusable result, therefore use knn as default prediction.
    else:
        return knn
    
def __if_subset(check:list, default):
    if set(check).issubset((set(set_5))):
        return 5
    elif set(check).issubset((set(set_6))):
        return 6
    else:
        return default