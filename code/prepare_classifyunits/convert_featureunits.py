import re


# Hier wird bei java noch irgendwo hinterlegt, wie die Featureunits generiert wurden, also in den hashcodes? wird gespeichert, wie die values
# für die verarbeitung gesetzt wurden (normalize = true etc...), vllt dohc eine klasse einrichten, die das speichert und setted und hinterlegt in db?


# elegantere Lösung finden? vllt gensim simple preprocessing für alles in einem (inkl remove whitespaces)
def replace(para) -> str:
    para = re.sub('\W+',' ', para)
    return para


# HIER VLLT NOCH EIN CHECKER, dass die CONFIGS AUCH WIRKLICH DIE ENTSPRECHENDEN WERTE HABEN; SONST DEFAULT SETZEN

def normalize(fus: list, normalize: bool) -> str:

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
        
        # Filter Numbers, wenn am Anfang un am Ende (index 0 und -1 des strings) digits stehen

        if fus[0].isdigit() and fus[-1].isdigit():
            fus[0] = 'NUM'
            fus[-1] = 'NUM'
        
        # Lower Case
        [fu.lower() for fu in fus]

    return fus

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

    