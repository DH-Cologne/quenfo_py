"""Script to split ClassifyUnits into sentences and added lexical data. Generate ExtractionUnits for each
ClassifyUnit. """

# ## Imports
from . import convert_extractionunits
from orm_handling.models import ExtractionUnits
from prepare_classifyunits.feature_units import convert_featureunits


# ### Main-Function for ExtractionUnit generation
def get_extractionunits(classifyunit: object) -> list:
    extractionunits = list()
    # split each ClassifyUnit into sentences
    sentences = convert_extractionunits.split_into_sentences(classifyunit.content)

    for sentence in sentences:
        sentence = convert_extractionunits.correct_sentence(sentence)
        # set lexical data
        token = convert_featureunits.tokenize(sentence)
        postags = convert_extractionunits.get_pos_tags(sentence)
        lemmata = convert_extractionunits.get_lemmata(sentence)

        if len(sentence) > 1:
            eu = ExtractionUnits(paragraph=classifyunit, sentence=sentence, token=token, posTags=postags,
                                 lemmata=lemmata)
            extractionunits.append(eu)
        classifyunit.children.append(eu)

    return extractionunits
