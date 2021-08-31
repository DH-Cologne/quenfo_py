"""Models using for information extraction."""
from enum import Enum
from pathlib import Path

import yaml


class Token:
    """Describes the attributes of a single token.
        A token contains the string representation (token), lemma and pos tag.
        Also, whether it is a known entity, a known bug, or a modifier."""
    token = str()
    pos_tag = str()
    lemma = str()

    modifier_token = bool()
    ie_token = bool()
    no_token = bool()

    # init-function to set values, works as constructor
    def __init__(self, token, lemma, pos_tag):
        self.token = token
        self.pos_tag = pos_tag
        self.lemma = lemma

    def set_ie_token(self, ie_token):
        self.ie_token = ie_token

    def set_modifier_token(self, modifier_token):
        self.modifier_token = modifier_token

    def set_no_token(self, no_token):
        self.no_token = no_token

    # string representation of a Token object
    def string_representation(self) -> str:
        return self.token


class Pattern:
    """Represents an Extraction-Pattern to identify Information (e.g. competences or tools) in JobAds. Consist of
    several PatternTokens and a Pointer to the Token(s) which has to be extracted in case of a match. """
    pattern_token = list()
    extraction_pointer = list()
    description = str()
    id = int()
    conf = float()

    def __init__(self, pattern_token, extraction_pointer, description, id):
        self.pattern_token = pattern_token
        self.extraction_pointer = extraction_pointer
        self.description = description
        self.id = id

    # compute confidence of an extraction pattern
    def set_conf(self, fp, tp) -> float:
        if tp == 0 and fp == 0:
            self.conf = 0.0
        else:
            self.conf = tp / (tp + fp)
        return self.conf

    # string representation of a Token object
    def string_representation(self) -> str:
        full_expression = "ID:\t" + str(self.id) + "\n" + "NAME:\t" + self.description + "\n"
        for token in self.pattern_token:
            full_expression += "TOKEN:\t" + token.token + "\t" + token.lemma + "\t" + token.pos_tag + "\t" \
                               + token.ie_token + "\t"
        full_expression += "EXTRACT:\t"
        for i in self.extraction_pointer:
            full_expression += str(i) + ","
        full_expression = full_expression[0:len(full_expression) - 1]
        full_expression += "\nCONF:\t" + self.conf + "\n\n"
        return full_expression


class PatternToken(Token):
    """Represents a single Token as part of an Extraction-Pattern. The attributes string, lemma and posTag can be
    null, if values are not specified in the pattern.
    Extends class Token."""

    # init-function to set values, works as constructor
    def __init__(self, token, lemma, pos_tag, ie_token):
        super(PatternToken, self).__init__(token, lemma, pos_tag)
        if ie_token:
            super(PatternToken, self).set_ie_token(True)

    # Modifier in pattern are described through string "IMPORTANCE"
    def get_lemma(self) -> str:
        if super(PatternToken, self).modifier_token:
            return "IMPORTANCE"
        return super(PatternToken, self).lemma

    #  string representation of a PatternToken object
    def string_representation(self) -> str:
        full_expression = super(PatternToken, self).token + "\t" + super(PatternToken, self).lemma + "\t" \
                          + super(PatternToken, self).pos_tag + "\t"
        if super(PatternToken, self).ie_token:
            full_expression += "isInformationEntity" + "\t"
        if super(PatternToken, self).modifier_token:
            full_expression += "is (start of) modifier" + "\t"

        return full_expression


class Configuration():
    """ Class to get the parameters set in config.yaml and check if they are valid.
            --> If not, set default values. """

    # ## Open Configuration-file and set variables + paths
    with open(Path('config.yaml'), 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)

        # get path from config
        resources = cfg['resources']
        input_path = resources['input_path']

        # competences
        competence_path = resources['competences_path']
        no_competence_path = resources['nocompetences_path']
        modifier_path = resources['modifier_path']
        comppattern_path = resources['comppattern_path']

        # tools
        tools_path = resources['tools_path']
        no_tools_path = resources['notools_path']
        toolpattern_path = resources['toolpattern_path']

        db_mode = cfg["mode"]
        query_limit = cfg["query_limit"]

        ie_config = cfg['ie_config']
        ie_type = ie_config['type']
        search = ie_config['search']
