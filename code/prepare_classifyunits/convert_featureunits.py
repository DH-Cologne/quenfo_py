# ## Imports
from pathlib import Path
import re
import py_stringmatching as sm
from contextlib import suppress
from nltk.stem.snowball import GermanStemmer

# ## Set Variables
sw_list = list()

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

def encode(fus: str) -> str:
    # alle non-asci zeichen werden ignoriert, spezifizierung für 33-122 ascii chars
    fus = fus.encode('ascii',errors='ignore').decode('ascii')
    return fus

def tokenize(fus: str) -> list:
    # TODO: Tokenization überlegen -->  delimiter = "[^\\pL\\pM\\p{Nd}\\p{Nl}\\p{Pc}[\\p{InEnclosedAlphanumerics}&&\\p{So}]]"; Tokenizes specified text into sequences of alphanumeric characters
    alnum_tok = sm.AlphanumericTokenizer()
    fus = alnum_tok.tokenize(fus)
    
    #fus = fus.split()
    return fus


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

def filterSW(fus: list, filterSW: bool, sw_path: Path) -> list:
    # fill stopwords list from file once
    __check_once(sw_path)
    # remove all stopwords from fus
    if filterSW:
        for sw in sw_list:
            with suppress(ValueError):
                # remove also duplicated sw in fus --> while True
                while True:
                    fus.remove(sw.lower())
    
    return fus

def __check_once(sw_path): 
        global sw_list
        if not sw_list:
            with open(sw_path, 'r') as sw_file:
                sw_list = [sw.strip() for sw in sw_file.readlines()]
        else:
            pass

# snowball stemmer nltk 
# TODO: Spacy als alternative ansehen
def stem(fus: list, stem: bool) -> list:
    stemmed_fus=list()
    if stem:
        stemmer = GermanStemmer()
        for token in fus:
            stemmed_fus.append(stemmer.stem(token))
        # TODO: stems = stemmed_fus --> Lösche Token, die bestimmte Größe haben?
        """ if(stems.get(stems.size()-1).length() <=1){
				stems.remove(stems.size()-1);
			} """
    return stemmed_fus 

def ngrams(fus: list, ngrams: int, cngrams: bool) -> list:
    if ngrams == int:
        fus = fus
    return fus
    