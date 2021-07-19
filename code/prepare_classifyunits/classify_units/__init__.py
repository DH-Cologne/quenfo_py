# ## Imports
from . import convert_classifyunits

# ## Functions

def get_paragraphs(jobad: object) -> list:
    """ 
    Step 1: Split at emtpy line
        --> Splits the text in jobad.content into Paragraphs at empty lines
    
    Step 2: remove whitespaces
        --> Removes whitespaces at the end and the beginning of a paragraph and each line
   
    
    Parameters
    ----------
    jobad: object
        object of the class JobAds which contains id, posting_id, jahrgang, language, content
    
    Returns
    -------
    list_paragraphs: list
        list with paragraphs for one jobad item """

    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad
    list_paragraphs = convert_classifyunits.split_at_empty_line(jobad)
    
    # 2. # Remove whitespaces at the beginning and at the end of each paragraph and in each line
    list_paragraphs = convert_classifyunits.remove_whitespaces(list_paragraphs)

    # Returns organized paragraphs for a jobad
    return list_paragraphs


def clean_paragraphs(list_paragraphs: list) -> list:
    """ 
    Step 3: identify_listitems: 
    Iterate over a list of paragraphs and compare one paragraph to the previous one. If both paragraphs contain certain list-characters
    (like * or _), the paragraphs are merged together to one paragraph.
    
    Step 4: identify_whatbelongstogether:
    Iterate over a list of paragraphs and compare one paragraph to the previous one. 
    If the previous one ends with a period and the current one starts with uppercase/isjobtitle both paragraphs are merged together to one paragraph.
    
    Parameters
    ----------
    list_paragraphs: list
        list with paragraphs for one jobad item
    
    Returns
    -------
    list_paragraphs: list
        list with better cleaned paragraphs for one jobad item """

    # ## Step 3: to merge ListItems Together
    list_paragraphs = convert_classifyunits.identify_listitems(list_paragraphs)

    # ## Step 4: to merge What Belongs Together
    list_paragraphs = convert_classifyunits.identify_whatbelongstogether(list_paragraphs)

    # return cleaned list (listitems and belongs) to generate_classifyunits()
    return list_paragraphs