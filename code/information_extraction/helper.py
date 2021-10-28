"""Script contains helper functions."""

# ## Imports
from information_extraction.models import ExtractedEntity
from information_extraction.prepare_resources import get_modifier
from information_extraction.prepare_resources.convert_entities import normalize_entities


# ## Functions
def remove_modifier(extraction: ExtractedEntity) -> None:
    """Function to remove modifier token from extractions.

            Parameters:
            ----------
                extraction: ExtractedEntity
                    Receives a found extraction

            Returns:
            -------
                None"""

    # set variables
    lemma_list = extraction.lemma_array     # list with all lemmas
    to_delete = list()  # return list
    skip = 0
    required = -1
    modifier = get_modifier()   # dict with modifier loaded from resource file

    # iterate over each lemma
    for t in range(len(lemma_list)):
        if t + skip >= len(lemma_list):
            break
        # normalize lemma
        lemma = normalize_entities(lemma_list[t + skip])
        # find all occurrences of lemma in modifier list
        matched_modifier = [value for key, value in modifier.items() if hash(lemma) == key]
        if matched_modifier:
            required = -1
            match = False
            # iterate over each occurrence
            for m in matched_modifier:
                # compare length of list with all lemmas
                if len(m.lemma_array) > len(lemma_list):
                    continue
                for i in range(len(m.lemma_array)):
                    mod_lemma = m.lemma_array[i]
                    try:
                        # compare modifier lemma and extraction lemma
                        match = hash(mod_lemma) == hash(normalize_entities(lemma_list[t + skip + i]))
                    except IndexError:
                        match = False
                    if not match:
                        break
                if match:
                    if len(m.lemma_array) > required:
                        required = len(m.lemma_array) - 1
            # if modifier is multi token
            if required > -1:
                to_delete.append(lemma)
                for j in range(required):
                    to_delete.append(lemma_list[t + skip + j])
                skip += required
    lemma_list.remove(to_delete)
    extraction.set_lemma_array(lemma_list)

    # set default
    to_delete = list()
    skip = 0
    required = -1


def is_all_upper(string: str) -> bool:
    """Function to check if character of given string is not letter or capitalized letter.

            Parameters:
            ----------
                string: str
                    Receives a string to check.

            Returns:
            -------
                bool if string is all upper or not"""

    string = string.replace('-', '')
    i = 0
    try:
        while True:
            #  character is either not a letter or a capitalized letter
            if not string[i].isalpha() or string[i].isupper():
                break
            i += 1
    except IndexError:
        return True

    return False
