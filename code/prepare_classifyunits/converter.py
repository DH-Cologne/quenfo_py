"""Script contains several functions used to preprocess the passed texts, objects, strings etc."""

# ## Imports
import re
from sys import prefix
from typing import Union


# Returns list of paragraphs per object
def split_at_empty_line(jobad: object) -> list:
    return jobad.content.split("\n\n")

# Remove whitespaces at the beginning and at the end of the string and in each line
def remove_whitespaces(list_paragraphs: list) -> list:
    cleaned_paralist = list()
    for para in list_paragraphs:
        newpara = list()
        newstring = str()
        parasplit = para.split('\n')
        for line in parasplit:
            line = line.strip()
            newpara.append(line + '\n')
        cleaned_paralist.append((newstring.join(newpara)).strip())
    return cleaned_paralist

# Merge Listitems together
def merge_listitems(previous: str, para: str, previous_to_remember: str) -> Union[str, str]:
    # If-condition to prevent duplicated entries in output
    if previous_to_remember.__contains__(previous):
        previous, previous_to_remember = __check_for_duplicates(previous, previous_to_remember)
        return previous, previous_to_remember
    # Check if two paragraphs contain the required list characters and join them if true.
    else:
        previous, previous_to_remember = __isListItem(previous, para, previous_to_remember)
        return previous, previous_to_remember

# Check if two paragraphs contain the required list characters and join them if true.
def __isListItem(previous, para, previous_to_remember):
    # Regex for list items at the end of a paragraph and if previous ends with ":" + current is a list item
    regex_previous = re.compile(r"((\n(\s)*((-\*|-|\*|\d(\.|\\)|\.\\)(\s)*)(\w)+$)|(\s+[^.!?]*[:]))")
    # Regex for list items at the beginning of a paragraph
    regex_para = re.compile(r"(^(\s)*((-\*|\+|-|\*|\d(\.|\\)|\.\\)(\s)*)\w*)")
    if regex_previous.search(previous) and regex_para.search(para):
        previous = "\n".join([previous, para])
        previous_to_remember = previous
        # return changed previous to write in output
        return previous, previous_to_remember
    else:
        # return unchanged previous to write in output
        return previous, previous_to_remember


# Check if the previous joined paragraph is used again. 
# If-condition to prevent duplicated entries in output
def __check_for_duplicates(previous, previous_to_remember):
    previous = ''
    previous_to_remember = ''
    return previous, previous_to_remember


def merge_whatbelongstogether(previous, para, previous_to_remember):
    if previous_to_remember.__contains__(previous):
        previous, previous_to_remember = __check_for_duplicates(previous, previous_to_remember)
        return previous, previous_to_remember
    # Check if two paragraphs contain the required list characters and join them if true.
    else:
        previous, previous_to_remember = __BelongsItem(previous, para, previous_to_remember)
        return previous, previous_to_remember

def __BelongsItem(previous, para, previous_to_remember):
    if previous != '' and previous_to_remember != '':
        if (previous.endswith('.') or previous.endswith(':')) and (para[0].isupper() or __looksLikeJobTitle(para)):
            print(previous)
            print(para)
            previous = "\n".join([previous, para])
            previous_to_remember = previous
            # return changed previous to write in output
            return previous, previous_to_remember
        else:
            return previous, previous_to_remember
    else:
        # return unchanged previous to write in output
        return previous, previous_to_remember

def __looksLikeJobTitle(para):
    regex_jobtitle = re.compile(r"^.*\w+/-?\w+.*$")
    return regex_jobtitle.match(para)