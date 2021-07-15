# ## Imports
from pathlib import Path
import re
import py_stringmatching as sm
from contextlib import suppress
from nltk.stem.snowball import GermanStemmer
from nltk import ngrams
from nltk.stem.cistem import Cistem

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


def tokenize(fus: str) -> list:
    
    WORD = re.compile(r'\w+')
    fus = WORD.findall(fus)
    
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


def stem(fus: list, stem: bool) -> list:
    # snowball stemmer nltk 
    stemmed_fus=list()
    if stem:
        # Snowball Stemmer from NLTK
        stemmer = GermanStemmer()
        for token in fus:
            stemmed_fus.append(stemmer.stem(token))
        
        # remove empty strings and strings <= 1
        stemmed_fus = list(filter(lambda n: 1 <= len(n), stemmed_fus))

        
        # TODO: Auch von NLTK: im Beispiel etwas schlecht --> In Klassifikation ausprobieren
        """ stemmer = Cistem()
        for token in fus:
            stemmed_fus.append(stemmer.segment(token)[0]) """

    return stemmed_fus 

def gen_ngrams(fus: list, ngram_numbers: dict, cngrams: bool) -> list:
    """ 	/**
	 * Generates ngrams from specified tokens.
	 * @param tokens List of tokens 
	 * @param n length of ngrams
	 * @param continuous If true, ngrams will be generated across token borders
	 * @return List of ngrams
	 */
	"""
    if type(list(ngram_numbers.keys())[0]) == int and type(list(ngram_numbers.keys())[1]) == int:
        # non continuous --> False, Token werden jeweils für sich verarbeitet
        if cngrams == False:
            ngrams_complete = list()
            for fu in fus:
                ngrams_store=list()
                # erst werden 3-gramme gebildet und dann 4-gramme (dafür steht {3,4})
                for ngram_nr in ngram_numbers:
                    for s in ngrams(fu,n=(ngram_nr)):        
                        ngrams_store.append(s)
                    ngrams_complete.extend(ngrams_store)
            fus = ngrams_complete
        else:   
            # continuous == True --> across token borders
            # whitespaces werden behalten und die token zu einem string zusammengefügt über den dann iteriert wird
            onestring = "".join(fus)
            ngrams_store= list()
            for ngram_nr in ngram_numbers:
                for s in ngrams(onestring,n=(ngram_nr)):        
                        ngrams_store.append(s)
            fus = ngrams_store
    return fus
    