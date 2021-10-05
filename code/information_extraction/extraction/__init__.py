from information_extraction.extraction.ie_jobs import extract, remove_known_entities, evaluate_pattern
from orm_handling.models import ExtractionUnits, InformationEntity


def extract_entities(extraction_unit: ExtractionUnits, ie_mode: str) -> 'list[InformationEntity]':
    extractions = extract(extraction_unit, ie_mode)

    extractions = remove_known_entities(extractions, ie_mode)

    evaluate_pattern()

    return extractions
