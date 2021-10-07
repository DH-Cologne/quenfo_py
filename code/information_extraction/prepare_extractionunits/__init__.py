"""Script to split ClassifyUnits into sentences and added lexical data. Generate ExtractionUnits for each
ClassifyUnit. """

# ## Imports
from . import convert_extractionunits
from orm_handling.models import ExtractionUnits, ClassifyUnits
from information_extraction.models import TextToken


def generate_extraction_units(classify_unit: ClassifyUnits, ie_mode: str) -> None:
    """Main-Function for ExtractionUnit generation.
            * Step 1: Split ClassifyUnit into sentences.
            * Step 2: Set lexical data (pos-tag, lemma) for each token of sentence.
            * Step 3: Store token with lexical data as TextToken object and adds to token array.
            * Step 4: Annotate token as known, fail or modifier.
            * Step 5: Store element as ExtractionUnit object.

            Parameters:
            ----------
                classifunit: ClassifyUnits
                    Receives an object from class ClassifyUnits.
                ie_mode: str
                    Receives an string with selected ie_mode.

            Returns:
            -------
                None"""

    position_index = 0

    # split each ClassifyUnit into sentences
    sentences = convert_extractionunits.split_into_sentences(classify_unit.paragraph)

    # iterate over each sentence
    for sentence in sentences:
        token_array = list()
        # normalize sentence
        sentence = convert_extractionunits.normalize_sentence(sentence)
        # set lexical data
        token = convert_extractionunits.get_token(sentence)
        postags = convert_extractionunits.get_pos_tags(sentence)
        lemmata = convert_extractionunits.get_lemmata(sentence)

        # collect all lexical data for one token and stores them in an TextToken-object
        for i, item in enumerate(token):
            if postags[i] is None:
                text_token = TextToken(token[i], lemmata[i], None)
                token_array.append(text_token)
            else:
                text_token = TextToken(token[i], lemmata[i], postags[i])
                token_array.append(text_token)

        # store last element
        token_array.append(TextToken(None, "<end-LEMMA>", "<end-POS>"))

        # annotate each token as known, fail or modifier
        token_array = convert_extractionunits.annotate_token(token_array, ie_mode)

        # Check if eu contains more than one string and if child does not exists
        if len(sentence) > 1 and not (any(sentence == v.sentence for v in classify_unit.children)):
            eu = ExtractionUnits(paragraph=classify_unit.paragraph, sentence=sentence, token_array=token_array,
                                 position_index=position_index, token=token, pos_tags=postags, lemmata=lemmata)
            classify_unit.children.append(eu)
            position_index += 1
            token_array = list()

    position_index = 0
