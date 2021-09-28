from information_extraction.prepare_resources import get_ie_pattern
from orm_handling.models import ExtractionUnits, InformationEntity


def extract_entities(extraction_unit: ExtractionUnits, ie_mode: str) -> 'list[InformationEntity]':
    extractions = list()
    pattern = get_ie_pattern(ie_mode)
    entity_pointer = int
    required_for_modifier = int
    required_for_entity = int
    match = bool

    eu_tokens = extraction_unit.token_array
    for p in pattern:
        if p.conf == 0.0 or p.conf >= 0.5:
            for i in range(len(eu_tokens) - p.get_size()):
                match = False
                entity_pointer = 0
                required_for_entity = 0
                required_for_modifier = 0
                for c in range(p.get_size()):
                    v = i + required_for_modifier + required_for_entity
                    if (v + c) >= len(eu_tokens):
                        continue
                    token = eu_tokens[v + c]
                    pattern_token = p.get_token_at_index(c)
                    match = token.is_equals_pattern_token(pattern_token)
                    if not match:
                        break
                    if p.extraction_pointer[0] == c:
                        entity_pointer = v + c
                    if pattern_token.ie_token:
                        required_for_entity = 0

    return extractions
