"""Script contains several functions used to preprocess the passed texts, objects, strings etc."""

# ## Imports
import re


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

