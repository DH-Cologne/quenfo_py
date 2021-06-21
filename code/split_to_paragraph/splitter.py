
import re
""" TODO: 
splitten wenn eine leere Zeile folgt (splitatemtpyline) 
→ dann wird aus dem Paragrafen ein sauberer String erstellt:
whitespaces am Anfang und am Ende eines Strings entfernen (trim() vs. strip())
lösche Zeilen, die keine nicht-alphanumerischen Zeichen enthalten (bspw. nur Sonderzeichen)
merge die List-items zsm
merge die Zeilen, bei denen die erste Zeile nicht mit einem Punkt endet und die zweite nicht mit uppercase char beginnt oder die ein Jobtitel ist
"""

# Returns list of paragraphs per object
def split_at_empty_line(jobad: object) -> list:
    return jobad.content.split("\n\n")

# Remove spaces at the beginning and at the end of the string
def remove_whitespaces(para: str) -> str:
    return para.strip()


# elegantere Lösung finden? vllt gensim simple preprocessing für alles in einem (inkl remove whitespaces)
def replace(para) -> str:
    para = re.sub('\W+',' ', para)
    return para