"""Models using for information extraction."""
from sqlalchemy import Column, String, Float

from orm_handling.models import InformationEntity


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


class TextToken(Token):
    tokensToCompleteInformationEntity = 0
    tokensToCompleteModifier = 0

    def __init__(self, token, lemma, pos_tag):
        super(TextToken, self).__init__(token, lemma, pos_tag)

    def set_ie_token(self, ie_token):
        super(TextToken, self).set_ie_token(ie_token)

    def set_modifier_token(self, modifier_token):
        super(TextToken, self).set_modifier_token(modifier_token)

    def set_no_token(self, no_token):
        super(TextToken, self).set_no_token(no_token)

    # string representation of a Token object
    def string_representation(self) -> str:
        return super(TextToken, self).string_representation()

    def is_equals_pattern_token(self, pattern_token) -> bool:
        if pattern_token.token is not None:
            pattern_strings = pattern_token.get_token().split(r'|')
            match = False
            for string in pattern_strings:
                match = string.__eq__(self.token)
                if match:
                    break
            if not match:
                return False
        elif pattern_token.pos_tag is not None:
            pattern_pos = pattern_token.pos_tag.split(r'|')
            if pattern_pos[0].startswith(r'-'):
                for pos in pattern_pos:
                    pos = pos[1: len(pos)]
                    if pos.__eq__(self.pos_tag):
                        return False
            else:
                match = False
                for pos in pattern_pos:
                    if pos.startswith(r'-'):
                        match = not (pos.__eq__(self.pos_tag))
                    else:
                        match = pos.__eq__(self.pos_tag)
                    if match:
                        break
                    if not match:
                        return False
        elif pattern_token.lemma is not None:
            if pattern_token.modifier_token:
                return self.modifier_token
            else:
                lemmas = pattern_token.lemma.split(r'|')
                match = False
                for lemma in lemmas:
                    if lemma.startswith(r'-'):
                        match = self.lemma.endswith(lemma[1: len(lemma)])
                        if match:
                            match = not (self.lemma.endswith(lemma[1: len(lemma)]))
                    else:
                        match = self.lemma.__eq__(lemma)
                    if match:
                        break
                if not match:
                    return False
        elif pattern_token.ie_token:
            return self.ie_token
        return True


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

    # return number of tokens of this pattern
    def get_size(self) -> int:
        return len(self.pattern_token)

    def get_token_at_index(self, index: int) -> Token:
        return self.pattern_token[index]

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
        full_expression += "\nCONF:\t", self.conf, "\n\n"
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

    def set_ie_token(self, ie_token):
        super(PatternToken, self).set_ie_token(ie_token)

    def set_modifier_token(self, modifier_token):
        super(PatternToken, self).set_modifier_token(modifier_token)

    def set_no_token(self, no_token):
        super(PatternToken, self).set_no_token(no_token)

    #  string representation of a PatternToken object
    def string_representation(self) -> str:
        full_expression = super(PatternToken, self).token + "\t" + super(PatternToken, self).lemma + "\t" \
                          + super(PatternToken, self).pos_tag + "\t"
        if super(PatternToken, self).ie_token:
            full_expression += "isInformationEntity" + "\t"
        if super(PatternToken, self).modifier_token:
            full_expression += "is (start of) modifier" + "\t"

        return full_expression


class ExtractedEntity(InformationEntity):
    conf = Column('conf', Float)
    pattern = Column('pattern_string', String(225))  # matched pattern description

    def __init__(self, pattern, ie_type, start_lemma, is_single_word):
        super(ExtractedEntity, self).__init__(ie_type, start_lemma, is_single_word)
        self.pattern = pattern

    # Setter
    def set_sentence(self, sentence: str):
        super(ExtractedEntity, self).set_sentence(sentence)

    def set_full_expression(self, full_expression: str):
        super(ExtractedEntity, self).set_full_expression(full_expression)

    def set_lemma_array(self, lemma_array: list):
        super(ExtractedEntity, self).set_lemma_array(lemma_array)

    def set_modifier(self, modifier: str):
        super(ExtractedEntity, self).set_modifier(modifier)

    def set_first_index(self, first_index: int):
        super(ExtractedEntity, self).set_first_index(first_index)

    def set_conf(self, used_pattern: 'list[Pattern]'):
        self.conf = 0.0
        product = 0.0
        conf_value = list()

        for pattern in used_pattern:
            conf_value.append(1 - pattern.conf)

        for i in range(len(conf_value)):
            if product == 0.0:
                product = conf_value[i]
            else:
                product = product * conf_value[i]
        self.conf = 1 - product


class MatchedEntity(InformationEntity):
    labels = set()

    def __init__(self, start_lemma, is_single_word, ie_type, label):
        super(MatchedEntity, self).__init__(ie_type=ie_type, start_lemma=start_lemma, is_single_word=is_single_word)
        self.labels = label

    # Setter
    def set_sentence(self, sentence: str):
        super(MatchedEntity, self).set_sentence(sentence)

    def set_full_expression(self, full_expression: str):
        super(MatchedEntity, self).set_full_expression(full_expression)

    def set_lemma_array(self, lemma_array: list):
        super(MatchedEntity, self).set_lemma_array(lemma_array)

    def set_modifier(self, modifier: str):
        super(MatchedEntity, self).set_modifier(modifier)

    def set_first_index(self, first_index: int):
        super(MatchedEntity, self).set_first_index(first_index)

    def add_label(self, label: str):
        self.labels.append(label)


class Modifier:
    start_lemma = str()
    lemma_array = list()
    is_single_word = bool()

    def __init__(self, start_lemma, is_single_word):
        self.start_lemma = start_lemma
        self.is_single_word = is_single_word

    def set_lemma_array(self, lemma_array):
        self.lemma_array = lemma_array
