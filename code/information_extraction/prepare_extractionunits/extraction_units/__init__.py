"""Script to split ClassifyUnits into sentences and added lexical data. Generate ExtractionUnits for each
ClassifyUnit. """

# ## Imports
from . import convert_extractionunits
from orm_handling.models import ExtractionUnits
from prepare_classifyunits.feature_units import convert_featureunits


# ### Main-Function for ExtractionUnit generation
from information_extraction.models import Token


def get_extractionunits(classifyunit: object) -> list:
    extractionunits = list()
    position_index = 0

    # split each ClassifyUnit into sentences
    sentences = convert_extractionunits.split_into_sentences(classifyunit.content)

    for sentence in sentences:
        token_array = list()
        sentence = convert_extractionunits.normalize_sentence(sentence)
        # set lexical data
        token = convert_featureunits.tokenize(sentence)
        postags = convert_extractionunits.get_pos_tags(sentence)
        lemmata = convert_extractionunits.get_lemmata(sentence)

        for i in range(len(token)):
            if postags is None:
                text_token = Token(token[i], lemmata[i], None)
                token_array.append(text_token)
            else:
                text_token = Token(token[i], lemmata[i], postags[i])
                token_array.append(text_token)

        token_array.append(Token(None, "<end-LEMMA>", "<end-POS>"))

        if len(sentence) > 1:
            eu = ExtractionUnits(paragraph=classifyunit, sentence=sentence, token=token, posTags=postags,
                                 lemmata=lemmata, token_array=token_array, position_index=position_index)
            extractionunits.append(eu)
        classifyunit.children.append(eu)
        position_index += 1

    position_index = 0

    return extractionunits
