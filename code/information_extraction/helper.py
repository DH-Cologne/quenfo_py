from information_extraction.models import ExtractedEntity
from information_extraction.prepare_resources import get_modifier
from information_extraction.prepare_resources.convert_entities import normalize_entities


def remove_modifier(extraction: ExtractedEntity):
    lemma_list = extraction.lemma_array
    to_delete = list()
    skip = 0
    required = -1
    modifier = get_modifier()
    for t in range(len(lemma_list)):
        if t + skip >= len(lemma_list):
            break
        lemma = normalize_entities(lemma_list[t + skip])
        matched_modifier = [m for m in modifier if m.start_lemma == hash(lemma)]
        if matched_modifier:
            required = -1
            match = False
            for m in matched_modifier:
                if len(m.lemma_array) > len(lemma_list):
                    continue
                for i in range(len(m.lemma_array)):
                    mod_lemma = m.lemma_array[i]
                    try:
                        match = mod_lemma.__eq__(normalize_entities(lemma_list[t + skip + i]))
                    except IndexError:
                        match = False
                    if not match:
                        break
                if match:
                    if len(m.lemma_array) > required:
                        required = len(m.lemma_array) - 1
            if required > -1:
                to_delete.append(lemma)
                for j in range(required):
                    to_delete.append(lemma_list[t + skip + j])
                skip += required
    lemma_list.remove(to_delete)
    extraction.set_lemma_array(lemma_list)

    to_delete = list()
    skip = 0
    required = -1
