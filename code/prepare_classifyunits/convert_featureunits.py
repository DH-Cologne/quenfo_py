import re


# Hier wird bei java noch irgendwo hinterlegt, wie die Featureunits generiert wurden, also in den hashcodes? wird gespeichert, wie die values
# für die verarbeitung gesetzt wurden (normalize = true etc...), vllt dohc eine klasse einrichten, die das speichert und setted und hinterlegt in db?


def replace(para: str) -> str:
    """ The replace function replaces all non-alphanumerical characters with a whitespace via regex

    Parameters
    ----------
    para: str
        para variable contains the paragraph of a jobad as string
    
    Returns
    -------
    para: str
        returns para variable without non-alphanumerical characters"""

    para = re.sub('\W+',' ', para)
    return para


# HIER VLLT NOCH EIN CHECKER, dass die CONFIGS AUCH WIRKLICH DIE ENTSPRECHENDEN WERTE HABEN; SONST DEFAULT SETZEN

def normalize(fus: list, normalize: bool) -> list:
    """ The normalization function contains 3 steps:
        a. lower case
        b. replace token with beginning and ending digits as characters with NUM
        c. append only token with more than one character to output list

    Parameters
    ----------
    fus: list
        the list contains the featureunits of a paragraph aka token
    normalize: boolean
        bool value from config to determine if normalization step is executed 
        
    Returns
    --------
    norm_fus: list
        list with normalized token, is used as fus for a paragraph """

    # normalized fus are stored in new list
    norm_fus = list()
    # Check if normalize is set to true and use the following normalization step
    if normalize:
        # for token in token_list
        for fu in fus:
            # Lower Case
            fu = fu.lower()
            # if token starts and ends with a digit-character --> set token to NUM because it won't be processable
            if fu[0].isdigit() and fu[-1].isdigit():
                fu = 'NUM'
            # filter 
            if len(fu) > 1:
                norm_fus.append(fu)
        return norm_fus
                
def stem(fus: list, stem: bool) -> list:
    if stem:
        fus = fus
    return fus 

def filterSW(fus: list, filterSW: bool) -> list:
    if filterSW:
        fus = fus
    return fus

def ngrams(fus: list, ngrams: int) -> list:
    if ngrams == int:
        fus = fus
    return fus

def cngrams(fus: list, cngrams: bool) -> list:
    if cngrams:
        fus = fus
    return fus

    