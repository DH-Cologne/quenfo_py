class Token:
    token = str
    pos_tag = str
    lemma = str

    modifier_token = bool
    ie_token = bool
    no_token = bool

    def __init__(self, token, lemma, pos_tag):
        self.token = token
        self.pos_tag = pos_tag
        self.lemma = lemma
