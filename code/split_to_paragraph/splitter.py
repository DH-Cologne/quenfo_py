""" TODO: 
splitten wenn eine leere Zeile folgt (splitatemtpyline) 
→ dann wird aus dem Paragrafen ein sauberer String erstellt:
whitespaces am Anfang und am Ende eines Strings entfernen (trim() vs. strip())
lösche Zeilen, die keine nicht-alphanumerischen Zeichen enthalten (bspw. nur Sonderzeichen)
merge die List-items zsm
merge die Zeilen, bei denen die erste Zeile nicht mit einem Punkt endet und die zweite nicht mit uppercase char beginnt oder die ein Jobtitel ist
"""
# sowas wie wie main, kann vllt in init
def jobads_to_paragraphs(jobads: list):
    for obj in jobads:
        split_at_empty_line(obj)


def split_at_empty_line(obj: object) -> list:
    list_paragraphs = obj.content.split("\n\n")
    return list_paragraphs