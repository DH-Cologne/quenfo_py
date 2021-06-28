import re


# Hier wird bei java noch irgendwo hinterlegt, wie die Featureunits generiert wurden, also in den hashcodes? wird gespeichert, wie die values
# für die verarbeitung gesetzt wurden (normalize = true etc...), vllt dohc eine klasse einrichten, die das speichert und setted und hinterlegt in db?


# elegantere Lösung finden? vllt gensim simple preprocessing für alles in einem (inkl remove whitespaces)
def replace(para) -> str:
    para = re.sub('\W+',' ', para)
    return para


# HIER VLLT NOCH EIN CHECKER, dass die CONFIGS AUCH WIRKLICH DIE ENTSPRECHENDEN WERTE HABEN; SONST DEFAULT SETZEN

def normalize(fu: str, normalize: bool) -> str:
    if normalize:
        """ if(normalizeNumbers && Character.isDigit(fu.charAt(0)) && Character.isDigit(fu.charAt(fu.length()-1))){
				fu="NUM";
			}
			if(toLowerCase){
				fu = fu.toLowerCase();
			}
			if(fu.length() > 1){
				featureUnits.set(i,fu);
			 """
        # Filter Numbers
        if fu.isdigit():
            fu = 'NUM'
        else:
            # Lower Case
            fu = fu.lower()
        print(fu)

    return fu

def stem(fu: str, stem: bool) -> str:
    if stem:
        fu = fu
    return fu 

def filterSW(fu: str, filterSW: bool) -> str:
    if filterSW:
        fu = fu
    return fu

def ngrams(fu: str, ngrams: int) -> str:
    if ngrams == int:
        fu = fu
    return fu

def cngrams(fu: str, cngrams: bool) -> str:
    if cngrams:
        fu = fu
    return fu

    