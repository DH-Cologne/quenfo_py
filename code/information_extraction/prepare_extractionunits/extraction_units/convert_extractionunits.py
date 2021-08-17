"""Script contains several functions used to preprocess the passed texts, objects, strings etc."""

# ## Imports
import spacy
import re

from prepare_classifyunits.classify_units import convert_classifyunits

# load nlp-model for sentence detection, pos tagger and lemmatizer
nlp = spacy.load("de_core_news_sm")
# ##Functions


# Split into Sentences
def split_into_sentences(content: str) -> list:
    """Get ExtractionUnits:
        +++ Step 1: Split Paragraph into Sentences. Take use of SentenceRecognizer from Spacy.+++

        Parameters:
        -----------
        content: str
            Receives the content of an ClassifyUnit-Object

        Returns:
        --------
        list
            list of sentences from the ClassifyUnit-Content"""

    extractionunits = list()
    # Construction from class and apply the SentenceRecognizer

    list_extractionunits = nlp(content)

    for eu in list_extractionunits.sents:
        # Paragraphs with list items will be separated as single sentences
        splitted = __split_list_items(str(eu))
        extractionunits.extend(splitted)

    # returns list with sentences from ClassifyUnit
    return extractionunits


# Split list items into single sentences
def __split_list_items(sentence: str) -> list:
    extractionunits = list()
    # split sentence at empty lines
    splitted_eu = convert_classifyunits.split_at_empty_line(sentence)
    # regex for match any existing list item in the sentence
    list_item_regex = re.compile(r"^[0-9][\\.| ]?|^[\+|\-|\*]")
    for string in splitted_eu:
        # remove whitespaces, tabstops etc.
        string = string.strip()
        # compare regex with given sentence
        m = re.match(list_item_regex, string)
        if m:
            # if regex matches, the list item is removed from the sentence
            string = string[m.end():]
            string = string.strip()
        if len(string) > 0 & __contains_only_word_characters(string):
            extractionunits.append(string)

    # returns the sentence without any list items
    return extractionunits


# check if sentence contains word characters
def __contains_only_word_characters(string: str) -> bool:
    # regex for word character
    word_regex = re.compile(r"\w")
    if re.match(word_regex, string):
        return True
    return False


# correct sentence
# TODO Beziehen sich diese Fälle auf Textkernel-Daten? Sind sie notwendig?
def correct_sentence(sentence: str) -> str:
    """Get ExtractionUnits:
            +++ Step 2: Correct specific elements of the sentence. +++

            Parameters:
            -----------
            sentence: str
                Receives a sentence as potential ExtractionUnit

            Returns:
            --------
            str
                given string with corrections """
    if sentence.__contains__("UND"):
        sentence = sentence.replace("UND", "und")
    if sentence.__contains__("ODER"):
        sentence = sentence.replace("ODER", "oder")
    regex = re.compile(" und[-|\\/| ][\\/| ]?[ ]?oder ")
    m = re.match(regex, sentence)
    if m:
        sentence = sentence.replace(m.group(), "oder")
    regex = " oder[-|\\/| ][\\/| ]?[ ]?und "
    m = re.match(regex, sentence)
    if m:
        sentence = sentence.replace(m.group(), "und")

    # TODO 3 weitere Fälle

    return sentence


# get POS-tag for each token of given sentence
def get_pos_tags(sentence: str) -> list:
    """Get ExtractionUnits:
                +++ Step 3: Get lexical data from tokens. +++

                Parameters:
                -----------
                sentence: str
                        Receives sentence as potential ExtractionUnit.

                Returns:
                --------
                list
                    list of POS-tags for each token"""
    pos_tags = list()

    pre_pos_tags = nlp(sentence)
    for token in pre_pos_tags:
        print(token.text, token.pos_)
        pos_tags.append(token.pos_)

    return pos_tags


# get lemma for each token of given sentence
def get_lemmata(sentence: str) -> list:
    """Get ExtractionUnits:
                    +++ Step 3: Get lexical data from tokens. +++

                    Parameters:
                    -----------
                    sentence: str
                        Receives sentence as potential ExtractionUnit.

                    Returns:
                    --------
                    list
                        list of lemma for each token"""
    lemmata = list()

    pre_lemmata = nlp(sentence)
    for token in pre_lemmata:
        print(token.text, token.lemma_)
        lemmata.append(token.lemma_)

    return lemmata
