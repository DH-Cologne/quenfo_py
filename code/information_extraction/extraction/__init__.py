from information_extraction.models import TextToken, ExtractedEntity, Token
from information_extraction.helper import remove_modifier
from information_extraction.prepare_resources import get_ie_pattern, get_no_entities
from information_extraction.prepare_resources.convert_entities import normalize_entities
from orm_handling.models import ExtractionUnits, InformationEntity


def extract_entities(extraction_unit: ExtractionUnits, ie_mode: str) -> 'list[InformationEntity]':
    extractions = list()
    pattern = get_ie_pattern(ie_mode)
    no_entities = get_no_entities(ie_mode)
    entity_pointer = int
    required_for_modifier = int
    required_for_entity = int
    match = bool
    entity_token = TextToken(lemma=str(), token=str(), pos_tag=str())

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
                        required_for_entity = token.tokensToCompleteInformationEntity
                    if pattern_token.modifier_token:
                        required_for_modifier = token.tokensToCompleteModifier
                if match:
                    entity_token = eu_tokens[entity_pointer]
                    print(entity_token)
                    norm_lemma = normalize_entities(entity_token.lemma)
                    entity_size = len(p.extraction_pointer)
                    if entity_size == 1:
                        if entity_token.modifier_token or entity_token.no_token:
                            continue
                        if len(norm_lemma) > 1 and not entity_token.lemma.__eq__('--'):
                            ie = ExtractedEntity(start_lemma=norm_lemma, is_single_word=True, ie_type=ie_mode,
                                                 pattern=p.description)
                            extraction_unit.children.append(ie)
                        else:
                            continue
                    else:
                        if len(norm_lemma) > 1 and not entity_token.lemma.__eq__('--'):
                            ie = ExtractedEntity(start_lemma=norm_lemma, is_single_word=False, ie_type=ie_mode,
                                                 pattern=p.description)
                            extraction_unit.children.append(ie)
                        else:
                            continue
                        complete_entity = list[Token]
                        for j in range(len(p.extraction_pointer)):
                            current_token = eu_tokens[entity_pointer + j]
                            norm_current_token = normalize_entities(current_token.lemma)
                            if not norm_current_token.strip().__eq__('') and not norm_current_token.strip().__eq__('--'):
                                complete_entity.append(norm_current_token)
                        if len(complete_entity) > 1:
                            # TODO Morphemkoordination hinzufügen
                            ie = ExtractedEntity(start_lemma=complete_entity[0], is_single_word=False, ie_type=ie_mode,
                                                 pattern=p.description)
                            extraction_unit.children.append(ie)
                            ie.lemma_array = complete_entity
                        elif len(complete_entity) < 1:
                            continue
                        else:
                            ie = ExtractedEntity(start_lemma=complete_entity[0], is_single_word=True, ie_type=ie_mode,
                                                 pattern=p.description)
                            extraction_unit.children.append(ie)
                        extractions.append(ie)
                    for e in extractions:
                        is_no_entity = False
                        if no_entities.__contains__(e.start_lemma):
                            is_no_entity = True
                        if is_no_entity:
                            e = None
                            continue
                        if ie_mode != 'TOOL':
                            remove_modifier(e)
                        if len(e.lemma_array) < 1:
                            e = None
                            continue
                        extractions.append(e)
    eu_tokens = None
    return extractions
