"""Script to split ClassifyUnits into sentences and added lexical data. Generate ExtractionUnits for each
ClassifyUnit. """

# ## Imports
from . import convert_extractionunits
from orm_handling.models import ExtractionUnits, ClassifyUnits
from information_extraction.models import TextToken

# ### Main-Function for ExtractionUnit generation


def get_extractionunits(classifyunit: ClassifyUnits, ie_mode: str):
    position_index = 0

    # split each ClassifyUnit into sentences
    sentences = convert_extractionunits.split_into_sentences(classifyunit.paragraph)

    for sentence in sentences:
        token_array = list()
        sentence = convert_extractionunits.normalize_sentence(sentence)
        # set lexical data
        token = convert_extractionunits.get_token(sentence)
        postags = convert_extractionunits.get_pos_tags(sentence)
        lemmata = convert_extractionunits.get_lemmata(sentence)

        for i, item in enumerate(token):
            if postags[i] is None:
                text_token = TextToken(token[i], lemmata[i], None)
                token_array.append(text_token)
            else:
                text_token = TextToken(token[i], lemmata[i], postags[i])
                token_array.append(text_token)

        token_array.append(TextToken(None, "<end-LEMMA>", "<end-POS>"))

        token_array = convert_extractionunits.annotate_token(token_array, ie_mode)

        if len(sentence) > 1 and not (any(sentence == v.sentence for v in classifyunit.children)):
            eu = ExtractionUnits(paragraph=classifyunit.paragraph, sentence=sentence, token_array=token_array,
                                 position_index=position_index, token=token, pos_tags=postags, lemmata=lemmata)
            classifyunit.children.append(eu)
            position_index += 1
            token_array = list()
    position_index = 0
