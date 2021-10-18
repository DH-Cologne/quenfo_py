"""Script manages the jobs from information extraction."""

# ## Imports
import configuration
from information_extraction.coordinate_expander import resolve
from information_extraction.models import TextToken, ExtractedEntity
from information_extraction.helper import remove_modifier
from information_extraction.prepare_resources import get_ie_pattern, get_no_entities, get_entities
from information_extraction.prepare_resources.convert_entities import normalize_entities
from orm_handling.models import ExtractionUnits, InformationEntity

# set variables
known_entities = dict()
no_entities = dict()


def extract(extraction_unit: ExtractionUnits, ie_mode: str) -> 'list[InformationEntity]':
    """Main-function for extraction.

            Parameters:
            ----------
                extraction_unit: ExtractionUnits
                    Receives an object from class ExtractionUnits.
                ie_mode: str
                    Receives an string with selected ie_mode.

            Returns:
            -------
                list with extractions of type InformationEntity"""

    # set global
    global no_entities

    # set variables
    extractions = list()    # return list
    pattern = get_ie_pattern(ie_mode)   # list with loaded pattern from resources
    no_entities = get_no_entities(ie_mode)  # list with loaded extraction fails from resources
    entity_pointer = int    # displays the location where an extraction was found
    required_for_modifier = int     # displays the number of tokens for complete modifier expression
    required_for_entity = int   # displays the number of tokens for complete entity expression
    match = bool    # variable for matched
    entity_token = TextToken(lemma=str(), token=str(), pos_tag=str())   # empty TextToken object for found extraction

    # get tokens from eu
    eu_tokens = extraction_unit.token_array

    # iterate over each pattern
    for p in pattern:
        # check if pattern has declared conf value
        if p.conf == 0.0 or p.conf >= 0.5:
            # iterate over each token
            for i in range(0, len(eu_tokens) - p.get_size()):
                # set default
                match = False
                entity_pointer = 0
                required_for_entity = 0
                required_for_modifier = 0
                # iterate over each token from pattern
                for c in range(p.get_size()):
                    v = i + required_for_modifier + required_for_entity
                    if (v + c) >= len(eu_tokens):
                        continue
                    token = eu_tokens[v + c]
                    pattern_token = p.get_token_at_index(c)
                    # check if current token equals current pattern token
                    match = token.is_equals_pattern_token(pattern_token)
                    if not match:
                        break
                    # if matched set variables
                    if p.extraction_pointer[0] == c:
                        entity_pointer = v + c
                    if pattern_token.ie_token:
                        required_for_entity = token.tokensToCompleteInformationEntity
                    if pattern_token.modifier_token:
                        required_for_modifier = token.tokensToCompleteModifier
                if match:
                    # set entity token as extraction
                    entity_token = eu_tokens[entity_pointer]
                    # normalized token
                    norm_lemma = normalize_entities(entity_token.lemma)
                    # set length of the following token
                    entity_size = len(p.extraction_pointer)
                    # single token
                    if entity_size == 1:
                        if entity_token.modifier_token or entity_token.no_token:
                            continue
                        # store extraction as ExtractedEntity object
                        if len(norm_lemma) > 1 and not entity_token.lemma == '--':
                            ie = ExtractedEntity(start_lemma=norm_lemma, is_single_word=True, ie_type=ie_mode,
                                                 pattern=p.description)
                            extraction_unit.children.append(ie)
                            extractions.append(ie)
                        else:
                            continue
                    # multi token
                    else:
                        if len(norm_lemma) > 1 and not entity_token.lemma == '--':
                            # store extraction as ExtractedEntity object
                            ie = ExtractedEntity(start_lemma=norm_lemma, is_single_word=False, ie_type=ie_mode,
                                                 pattern=p.description)
                            extraction_unit.children.append(ie)
                            extractions.append(ie)
                        else:
                            continue
                        complete_entity = list()
                        # stores all token from extraction
                        for j in range(len(p.extraction_pointer)):
                            current_token = eu_tokens[entity_pointer + j]
                            # normalized token
                            norm_current_token = normalize_entities(current_token.lemma)
                            if not norm_current_token.strip() == '' and not norm_current_token.strip() == '--':
                                complete_entity.append(current_token)

                        if len(complete_entity) > 1:    # entity consists of more than one token
                            coordinate_entities = list()

                            # check if it is a morpheme coordination
                            for e in complete_entity:
                                # as long as no TRUNC appears, all lemmas are added to the expression
                                coordinate_entities.append(normalize_entities(e.lemma))
                                # as soon as a KON appears, the morpheme coordination is resolved
                                if configuration.config_obj.get_expand_coordinates() and e.pos_tag == 'KON':
                                    combinations = resolve(complete_entity, eu_tokens, False)

                                    # for each expansion an InformationEntity is created
                                    for combination_list in combinations:
                                        combination_lemmata = list()
                                        
                                        for c_token in combination_list:
                                            combination_lemmata.append(c_token.lemma)
                                        ie = ExtractedEntity(start_lemma=combination_lemmata[0], is_single_word=False,
                                                             ie_type=ie_mode, pattern=p.description)
                                        ie.set_lemma_array(combination_lemmata)
                                        extraction_unit.children.append(ie)
                                        extractions.append(ie)

                            # store extraction as ExtractedEntity object
                            ie = ExtractedEntity(start_lemma=complete_entity[0], is_single_word=False, ie_type=ie_mode,
                                                 pattern=p.description)
                            ie.first_index = entity_pointer
                            ie.lemma_array = complete_entity
                            extraction_unit.children.append(ie)
                            extractions.append(ie)
                        elif len(complete_entity) < 1:
                            continue
                        # single token
                        else:
                            # store extraction as ExtractedEntity object
                            ie = ExtractedEntity(start_lemma=complete_entity[0], is_single_word=True, ie_type=ie_mode,
                                                 pattern=p.description)
                            ie.first_index = entity_pointer
                            extraction_unit.children.append(ie)
                            extractions.append(ie)
                    for e in extractions:
                        # check if list with fails contains found extractions
                        is_no_entity = False
                        if hash(e.start_lemma) in no_entities.keys():
                            is_no_entity = True
                        if is_no_entity:
                            e = None
                            continue
                        if ie_mode != 'TOOL':
                            # remove modifier from extraction
                            remove_modifier(e)
                        if len(e.lemma_array) < 1:
                            e = None
                            continue
                        extractions.append(e)
    eu_tokens = None
    return extractions


def remove_known_entities(extractions: list, ie_mode: str) -> 'list[InformationEntity]':
    """Function to remove known entities from list with extractions.

            Parameters:
            ----------
                extractions: list
                    Receives a list with found extraction in EU.
                ie_mode: str
                    Receives an string with selected ie_mode.

            Returns:
            -------
                list with remaining InformationEntity objects"""

    # set global
    global known_entities

    # set variables
    known_entities = get_entities(ie_mode)  # list with known entities loaded from resources
    filtered_extractions = list()   # return list

    # iterate over each extraction
    for e in extractions:
        # search all occurrences of extraction in list
        matched_entities = [value for key, value in known_entities.items() if hash(e.start_lemma) == key]
        # remove all occurrences
        if matched_entities is None or not matched_entities.__contains__(e):
            filtered_extractions.append(e)
    return filtered_extractions


def evaluate_pattern(extractions: list) -> None:
    """Function to evaluate used pattern for extraction and set confidence value.

            Parameters:
            ----------
                extractions: list
                    Receives a list with found extraction in EU.

            Returns:
            -------
                None"""

    used_pattern = list()

    # iterate over each extraction and fill list with used pattern (no duplicates)
    for e in extractions:
        if not used_pattern.__contains__(e.pattern):
            used_pattern.append(e.pattern)

    # iterate over each used pattern and fill list with found extraction through pattern
    for p in used_pattern:
        found_extractions = list()
        for e in extractions:
            if e.pattern == p and not found_extractions.__contains__(e):
                found_extractions.append(e)

        # set variables with default
        tp = 0  # number of found extractions in list with known entities
        fp = 0  # number of found extractions in list with fails

        # iterate over each extraction from pattern
        for ie in found_extractions:

            # search all occurrences of extraction in list and add number
            matched_entities = [value for key, value in known_entities.items() if hash(ie.start_lemma) == key]
            tp += len(matched_entities)

            # search all occurrences of extraction in list and add number
            matched_no_entities = [value for key, value in no_entities.items() if hash(ie.start_lemma) == key]
            fp += len(matched_no_entities)

        # set conf value
        p.set_conf(fp, tp)

        tp = 0
        fp = 0


def evaluate_seeds(extractions: list) -> None:
    """Function to evaluate extractions and set confidence value.

            Parameters:
            ----------
                extractions: list
                    Receives a list with found extraction in EU.

            Returns:
            -------
                None"""

    all_extractions = list()

    # iterate over each extraction and fill list with all extractions (no duplicates)
    for ie in extractions:
        if all_extractions is []:
            all_extractions.append(ie)
        elif not any(e.start_lemma in all_extractions for e in ie.start_lemma):
            all_extractions.append(ie)

    # iterate over each extraction and fill list with used pattern
    for e in all_extractions:
        used_pattern = list()
        for ie in extractions:
            if e == ie:
                used_pattern.append(ie.pattern)

        # set conf
        e.set_conf(used_pattern)


def select_best_extractions(extractions: list) -> 'list[InformationEntity]':
    """Function to select extractions with specific confidence value.

            Parameters:
            ----------
                extractions: list
                    Receives a list with found extraction in EU.

            Returns:
            -------
                list with InformationEntity objects that reached conf"""

    # iterate over each extraction and check conf value
    for ie in extractions:
        if not ie.conf >= 0.5:
            extractions.remove(ie)

    return extractions
