"""Script contains several functions used to preprocess the passed texts, objects, strings etc."""

# ## Imports
import re
from typing import Union
import logger


# ## Functions

# Split into paragraphs
def split_at_empty_line(jobad_content: str) -> list:
    """ Get Paragraphs:
        +++ Step 1: Split at emtpy line +++ 
        
    Parameters
    ----------
    jobad_content: str
        Receives a jobad string
    
    Returns
    -------
    list
        list of paragraphs from the jobad_content text """
    
    # Returns list of paragraphs per object
    return jobad_content.split("\n\n")


# Remove whitespaces
def remove_whitespaces(list_paragraphs: list) -> list:
    """ Get Paragraphs:
        +++ Step 2: Remove Whitespaces +++ 

        Parameters
        ----------
        list_paragraphs: list
            list with paragraphs of one jobad
        
        Returns
        -------
        cleaned_paralist: list
            list of cleaned paragraphs from one jobad without whitespaces at the beginning and ending of each line"""

    # Set list for return statement
    cleaned_paralist = list()
    try:
        # Iterate over each paragraph
        for para in list_paragraphs:
            # Set list for cleaned paragraph
            newpara = str()
            # split paragraph after each line, remove whitespaces (beg and end) of each line, join the lines back
            # together and strip again the new paragraph --> append cleaned paragraph back on cleaned_paralist
            cleaned_paralist.append((newpara.join([(line.strip() + '\n') for line in para.split('\n')])).strip())
    except Exception as err:
        logger.log_clf.warning(f'While removing whitespaces error {err} raised. Except it and continue with paragraph.')
    return cleaned_paralist


# Merge Listitems
def identify_listitems(list_paragraphs: list) -> list:
    """ Clean Paragraphs:
        +++ Step 3: Merge List Items +++ 
        Compare two paragraphs and if they both have specific list-characteristics, merge those two together
        
    Parameters
    ----------
    list_paragraphs: list
        receives list of paragraphs from one jobad
    
    Returns
    -------
    cleaned_merged: list
        returns list with new paragraphs (partially merged) """

    # ## Set variables
    cleaned_merged = list()                         # List to store cleaned paragraphs
    i = 1                                           # counter
    list_paragraphs.insert(0, '')                   # add an empty string at the beginning and ending of the list for easier iteration
    list_paragraphs.append('')
    # set memory variable
    previous_to_remember = str()

    while i < len(list_paragraphs):
        # set variables to compare
        para = list_paragraphs[i]
        previous = list_paragraphs[i - 1]
        # Merge Listitems together
        para, previous_to_remember = __merge_listitems(previous, para, previous_to_remember)
        # append merged or old paragraph to output list
        cleaned_merged.append(para)
        i += 1

    # remove empty strings 
    # --> works as exception handling for regex too, because regex will no longer raise error but instead return None
    cleaned_merged = list(filter(None, cleaned_merged))
    return cleaned_merged


# Merge Listitems together
def __merge_listitems(previous: str, para: str, previous_to_remember: str) -> Union[str, str]:
    # approach to eliminate overwriting --> does previous_to_remember contain previous?
    if previous_to_remember.__contains__(previous):
        previous = previous_to_remember = ''
        return previous, previous_to_remember
    # Check if two paragraphs contain the required list characters and join them if true.
    else:
        previous, previous_to_remember = __isListItem(previous, para, previous_to_remember)
        return previous, previous_to_remember


# Check if two paragraphs contain the required list characters and join them if true.
def __isListItem(previous, para, previous_to_remember):
    """ Regex for list items at the end of a paragraph (regex_para) or 
    if previous ends with ":" or contains only one line ending (regex_previous) """

    # Regex to match with ":" (e.g. "Benötigte Anforderungen:") or one liner
    regex_previous = re.compile(r"(.*)[:]$|((-\*|-|\*|\d(\.|\\)|\.\\)(.*)$)")
    # Regex to match string that contains only list-items
    regex_para = re.compile(r"(^((\s)*(-\*|\+|-|\*|\d(\.|\\)|\.\\)(.*))+$)")

    # Compare paragraph and the previous paragraph, if they match --> join them (Escaping important!)
    if regex_previous.match(re.escape(previous)) and regex_para.match(re.escape(para)):
        previous = "\n".join([previous, para])
        # Set joined paragraphs as previous_to_remember => approach to eliminate overwriting
        previous_to_remember = previous
        # return changed previous to write in output
        return previous, previous_to_remember
    else:
        # return unchanged previous to write in output
        return previous, previous_to_remember


# Merge WhatBelongsTogether
def identify_whatbelongstogether(list_paragraphs: list) -> list:
    """ Clean Paragraphs:
        +++ Step 4: Merge What Belongs Together +++
        Check if two paragraphs contain the required charactistics 
        (previous !ends with '.' and para is !upper or jobtitle) and join them if true.
    
    Parameters
    ----------
    list_paragraphs: list
        receives list of paragraphs from one jobad (already with merged listitems)
    
    Returns
    -------
    belongs: list
        returns list with new paragraphs (partially merged) """

    # ## Set variables
    belongs = list()                        # List to store cleaned paragraphs
    i = 1                                   # counter
    list_paragraphs.insert(0, '')           # add an empty string at the beginning and ending of the list for easier iteration
    list_paragraphs.append('')
    # set memory variable
    previous_to_remember = str()

    while i < len(list_paragraphs):
        # set variables to compare
        para = list_paragraphs[i]
        previous = list_paragraphs[i - 1]
        # Merge Listitems together
        para, previous_to_remember = __merge_whatbelongstogether(previous, para, previous_to_remember)
        # append merged or old paragraph to output list
        belongs.append(para)
        i += 1

    # remove empty strings
    # --> works as exception handling for regex too, because regex will no longer raise error but instead return None
    belongs = list(filter(None, belongs))
    return belongs


def __merge_whatbelongstogether(previous, para, previous_to_remember):
    # If-condition to prevent duplicated entries in output
    if previous_to_remember.__contains__(previous):
        previous = previous_to_remember = ''
        return previous, previous_to_remember
    # Check if two paragraphs contain the required charactistics (previous ends with '.' or ':' and para is upper or
    # jobtitle) and join them if true.
    else:
        previous, previous_to_remember = __BelongsItem(previous, para, previous_to_remember)
        return previous, previous_to_remember


def __BelongsItem(previous, para, previous_to_remember):
    if previous != '' and para != '':
        if (not previous.endswith('.')) and (not para[0].isupper() or __looksLikeJobTitle(para)):
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
    # Regex to match strings as jobtitles (e.g. Bewerber:innen, Bewerber(w/m), Bewerber*innen...)
    regex_jobtitle = re.compile(r"^(.*)[\(.*\)|/|\*|:|/-].*$")
    return regex_jobtitle.match(re.escape(para))