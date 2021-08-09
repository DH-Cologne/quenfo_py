from . import convert_extractionunits


def get_extractionunits(classifyunit: object) -> list:
    list_extractionunits = convert_extractionunits.tokenize(classifyunit.content)

    return list_extractionunits
