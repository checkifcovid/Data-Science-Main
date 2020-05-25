

def get_true_positives_etc(y_actual, y_predict, dict_out=False):
    """
    Calculates true positives, true negatives, etc.
    """
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for y, y_p in zip(y_actual, y_predict):
        if y==y_p==1:
            TP += 1
        if y==y_p==0:
            TN += 1
        if y==0 and y_p==1:
            FP+=1
        if y==1 and y_p==0:
            FN+=1

    # How do you want it formated on output?
    if dict_out:
        return {"TP":TP,"TN":TN, "FP":FP,"FN":FN}

    else:
        return (TP, TN, FP, FN)
