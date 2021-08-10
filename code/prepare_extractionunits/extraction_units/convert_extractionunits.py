import spacy
import re

from prepare_classifyunits.classify_units import convert_classifyunits


def split_into_sentences(content: str) -> list:
    extractionunits = list()
    # Construction from class
    nlp = spacy.load("de_core_news_sm")
    list_extractionunits = nlp(content)

    for eu in list_extractionunits.sents:
        splitted = __split_list_items(str(eu))
        extractionunits.extend(splitted)

    return extractionunits


def __split_list_items(sentence: str) -> list:
    extractionunits = list()
    splitted_eu = convert_classifyunits.split_at_empty_line(sentence)
    list_item_regex = re.compile(r"(^(-\*|\+|-|\*))")
    for string in splitted_eu:
        string = string.strip()
        m = re.match(list_item_regex, string)
        if m:
            string = string[m.end():]
            print(string)
            string = string.strip()
        if len(string) > 0:
            extractionunits.append(string)

    return extractionunits


def __contains_only_non_word_characters(string: str) -> bool:
    word_regex = re.compile(r"\w")
    if re.match(word_regex, string):
        return True
    return False
