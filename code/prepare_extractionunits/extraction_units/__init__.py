from . import convert_extractionunits


def get_extractionunits(classifyunit: object) -> list:
    extractionunits = list()
    sentences = convert_extractionunits.split_into_sentences(classifyunit.content)

    return extractionunits
