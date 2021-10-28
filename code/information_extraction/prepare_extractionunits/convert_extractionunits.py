"""Script contains several functions used to preprocess the passed texts, objects, strings etc."""

# ## Imports
import spacy
import re
from information_extraction.models import TextToken
from information_extraction.prepare_resources import get_entities, get_no_entities, get_modifier
from information_extraction.prepare_resources.convert_entities import normalize_entities

# load nlp-model for sentence detection, pos tagger and lemmatizer
nlp = spacy.load("de_core_news_sm")

# set variables
known_entities = dict()
no_entities = dict()
modifier = dict()


# ## Functions
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


# Private function to split list items into single sentences
def __split_list_items(sentence: str) -> list:
    extractionunits = list()
    # split sentence at empty lines
    splitted_eu = __split_at_empty_line(sentence)
    # regex for match any existing list item in the sentence
    list_item_regex = re.compile(r"^[0-9][\.| ]?|^[\+|\-|\*]")
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


# Private funtion to check if sentence contains word characters
def __contains_only_word_characters(string: str) -> bool:
    # regex for word character
    word_regex = re.compile(r"\w")
    if re.match(word_regex, string):
        return True
    return False


# Private funtion to split sentence at empty line
def __split_at_empty_line(content: str) -> list:
    return content.split("\n")


def normalize_sentence(sentence: str) -> str:
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

    # 'und'/'oder' in uppercase change to be lowercase
    if sentence.__contains__("UND"):
        sentence = sentence.replace("UND", "und")
    if sentence.__contains__("ODER"):
        sentence = sentence.replace("ODER", "oder")

    # 'und/oder' in sentence change to be 'oder'
    regex = re.compile(r"^.*( und[\-|\/| ][\/| ]?[ ]?oder )")
    m = re.match(regex, sentence)
    if m:
        sentence = sentence.replace(m.group(1), " oder ")

    # 'oder/und' in sentence change to be 'und'
    regex = re.compile(r"^.*( oder[\-|\/| ][\/| ]?[ ]?und )")
    m = re.match(regex, sentence)
    if m:
        sentence = sentence.replace(m.group(1), " und ")

    # normalizes dot or comma if there is a space before them but none after them
    # adds a space after dot or comma
    regex = re.compile(r"^.*(\s[\.|\,])(\w+)")
    m = re.match(regex, sentence)
    if m:
        # exception: .NET (Microsoft-Framework)
        if m.group(2).lower() != "net":
            sentence = sentence.replace(m.group(1), m.group(1) + " ")

    # if there is a comma or semicolon without a space between two words,
    # a space is inserted after the comma or semicolon
    regex = re.compile(r"^.*[A-Za-z]+([\,|\;])[A-Za-z]+")
    m = re.match(regex, sentence)
    if m:
        sentence = sentence.replace(m.group(1), m.group(1) + " ")

    # checks the sentence for occurrences of / and * followed by two word characters and preceded by a space character
    # and normalizes them
    # e.g. Entwickler *in -> Entwickler/in
    regex = re.compile(r"^.*(\s[\/|\*])(\w\w)")
    m = re.match(regex, sentence)
    if m:
        if m.group(2) != "in":
            sentence = sentence.replace(m.group(1), " ")
        else:
            sentence = sentence.replace(m.group(1), "/")

    return sentence


def get_token(sentence: str) -> list:
    """Get ExtractionUnits:
                +++ Step 3: Get lexical data from tokens. +++

                Parameters:
                -----------
                sentence: str
                    Receives sentence as potential ExtractionUnit.

                Returns:
                --------
                list
                    list of token"""
    tokens = list()

    pre_token = nlp(sentence)
    for token in pre_token:
        tokens.append(token.text)

    return tokens


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
        pos_tags.append(token.pos_)

    return pos_tags


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
        lemmata.append(token.lemma_)

    return lemmata


def annotate_token(token: list, ie_mode: str) -> 'list[TextToken]':
    """Get ExtractionUnits:
                +++ Step 4: Annotate tokens by comparing them with list of extraction errors,
                modifiers and known extractions. +++

                Parameters:
                -----------
                token: list of Token
                    Receives list with tokens from ExtractionUnit
                ie_mode: str
                    Receives a string with the current extraction mode: competences or tools"""

    # set globals
    global known_entities, no_entities, modifier

    # get data from resource
    known_entities = get_entities(ie_mode)
    no_entities = get_no_entities(ie_mode)
    modifier = get_modifier()

    # call different methods depending on the list
    if known_entities:
        token = __annotate_entities(token)
    if no_entities:
        token = __annotate_negatives(token)
    # modifier only used by competence extraction
    if ie_mode != 'TOOLS' and modifier:
        token = __annotate_modifier(token)

    return token


# Private funtion to annotate token as known entity
def __annotate_entities(token: list) -> 'list[TextToken]':

    for i in range(len(token)):
        # each token will be normalized
        lemma = normalize_entities(token[i].lemma)
        # search all occurrences of the normalized token in list
        matched_entities = [value for key, value in known_entities.items() if hash(lemma) == key]
        for known_entity in matched_entities:
            if known_entity.is_single_word:
                # if known_entity is single word (e.g. 'wlan'), token the token also consists of only one
                token[i].set_ie_token(True)
                continue
            matches = False
            # otherwise it will be a multi token (e.g. 'software deployment')
            for j in range(len(known_entity.lemma_array)):
                # each following token is considered
                if len(token) <= i + j:
                    matches = False
                    break
                matches = hash(known_entity.lemma_array[j]) == (hash(normalize_entities(token[i + j].lemma)))
                if not matches:
                    break
            if matches:
                token[i].set_ie_token(True)
                token[i].tokensToCompleteInformationEntity = len(known_entity.lemma_array) - 1

    return token


# Private function to annotate token as known extraction fail
def __annotate_negatives(token: list) -> 'list[TextToken]':

    for i in range(len(token)):
        # each token will be normalized
        lemma = normalize_entities(token[i].lemma)
        # check if list contains normalized token
        if hash(lemma) in no_entities.keys():
            token[i].set_no_token(True)

    return token


# Private function to annotate token as modifier
def __annotate_modifier(token: list) -> 'list[TextToken]':

    for i in range(len(token)):
        # each token will be normalized
        lemma = normalize_entities(token[i].lemma)
        # search all occurrences of the normalized token in dict
        matched_modifier = [value for key, value in modifier.items() if hash(lemma) == key]
        for mod in matched_modifier:
            if mod.is_single_word:
                # if modifier is single word (e.g. 'erforderlich'), token the token also consists of only one
                token[i].set_modifier_token(True)
                continue
            matches = False
            # otherwise it will be a multi token (e.g. 'ideal aber kein bedingung')
            for j in range(len(mod.lemma_array)):
                # each following token is considered
                if len(token) <= i + j:
                    matches = False
                    break
                matches = hash(mod.lemma_array[j]) == hash(normalize_entities(token[i + j].lemma))
                if not matches:
                    break
            if matches:
                token[i].set_modifier_token(True)
                token[i].tokensToCompleteModifier = len(mod.lemma_array) - 1

    return token
