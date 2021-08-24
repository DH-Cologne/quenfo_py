"""Models using for information extraction."""


class Token:
    """Describes the attributes of a single token.
        A token contains the string representation (token), lemma and pos tag.
        Also, whether it is a known entity, a known bug, or a modifier."""
    token = str
    pos_tag = str
    lemma = str

    modifier_token = bool
    ie_token = bool
    no_token = bool

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
    description = str
    id = int
    conf = float


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
        full_expression = super(PatternToken, self).token + r"\t" + super(PatternToken, self).lemma + r"\t" \
                          + super(PatternToken, self).pos_tag + r"\t"
        if super(PatternToken, self).ie_token:
            full_expression += "isInformationEntity" + r"\t"
        if super(PatternToken, self).modifier_token:
            full_expression += "is (start of) modifier" + r"\t"

        return full_expression
