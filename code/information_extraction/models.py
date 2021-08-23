class Token:
    token = str
    pos_tag = str
    lemma = str

    modifier_token = bool
    ie_token = bool
    no_token = bool

    def __init__(self, token, lemma, pos_tag, modfier_token, ie_token, no_token):
        self.token = token
        self.pos_tag = pos_tag
        self.lemma = lemma
        self.modifier_token = modfier_token
        self.ie_token = ie_token
        self.no_token = no_token
