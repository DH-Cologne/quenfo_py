import logger


def resolve(complete_entity, eu_entities, debug: bool) -> list:
    token = list()
    pos_tags = list()
    lemmata = list()

    for i in range(len(complete_entity)):
        token[i] = complete_entity.token[i]
        pos_tags[i] = complete_entity.pos_tag[i]
        lemmata[i] = complete_entity.lemma[i]

    if debug:
        logger.log_ie.info(f'Entity Tokens: {token}')

    if pos_tags.__contains__('TRUNC'):
        return __resolve_trunc_ellipsis(token, pos_tags, lemmata, eu_entities, debug)


def __resolve_trunc_ellipsis(token: list, pos_tags: list, lemmata: list, eu_entities: list, debug: bool) -> list:
    """Function for morpheme coordination for right ellipsis.

            Parameters
            ----------
                token: list
                    Receives a list with token of the extraction.
                pos_tags: list
                    Receives a list with pos tags of the extraction.
                lemmata: list
                    Receives a list with lemmata of the extraction.
                eu_entities: list[TextToken]
                    Receives a list of TextToken objects from ExtractionUnit where extraction is found.
                debug: bool
                    Information about Debugging.

            Returns
            -------
                list with resolution of ellipsis"""

    resolved_token = list()
    start_koo = pos_tags.index('TRUNC')
    koo_string = token[start_koo]
    konjunct_pos = str()

    # check whether it is the coordination of NN or ADJA
    if koo_string[0].isupper():
        try:
            konjunct_pos = 'NN'
            # check if there is an ADJA before first NN
            if pos_tags[start_koo - 1] == 'ADJA':
                start_koo -= 1
        except IndexError:
            if debug:
                logger.log_ie.info(f'IndexError: No token at index before NN available.')
    else:
        konjunct_pos = 'ADJA'

    # determine end of coordination
    end_koo = pos_tags[start_koo: len(pos_tags)].index(konjunct_pos)
    if end_koo < 0:     # if coordination is cut off
        missing_part = __complete_coordinate(eu_entities, token, konjunct_pos)
        for t in missing_part:
            token.append(t.token)
            pos_tags.append(t.pos_tag)
            lemmata.append(t.lemma)

        end_koo = len(token) - 1
    else:
        end_koo = end_koo + start_koo   # because of subList index

    # tokens that are in front of the coordination
    before = list()
    for i in range(len(token)):
        if i > start_koo:
            break
        before.append(token[i])

    # tokens that stand after the coordination
    after = list()
    for i, item in enumerate(token, start=end_koo + 1):
        after.append(token[i])

    if debug:
        print(f'Before: {before}\n After: {after}')

    # collects all conjunct-modifier pairs (0 = modifier, 1 = trunc/nn/adja)
    conjuncts = list()
    conjunct = list()
    current_mod = ''
    pos_to_ignore = list()
    pos_to_ignore.append('KON')
    pos_to_ignore.append('$,')
    start_new_conjunct = True

    for i in range(start_koo, end_koo):
        if pos_tags[i] == 'TRUNC' or pos_tags[i] == konjunct_pos:
            conjunct[0] = current_mod.strip()
            conjunct[1] = token[i]
            conjuncts.append(conjunct)
            conjunct = list()
            start_new_conjunct = True
        elif pos_to_ignore.__contains__(pos_tags[i]):
            continue
        else:
            if start_new_conjunct:
                current_mod = token[i].strip()
            else:
                current_mod = current_mod + " " + token[i]
            start_new_conjunct = False

    # resolve coordinations
    coordinates = __combine_coordinates(conjuncts)

    return resolved_token


def __complete_coordinate(eu_entities: list, token: list, konjunct_pos: str) -> list:
    """Identifies the truncated tokens by their pos tags.

            Parameters:
            ----------
                eu_entities: list[TextToken]
                    Receives a list of TextToken objects from ExtractionUnit where extraction is found.
                token: list
                    Receives a list with token of the extraction.
                konjunct_pos: str
                    Receives a string with pos tag of conjunction.

            Returns:
            -------
                list with complete coordinate"""

    missing_part = list()

    for i in range(len(eu_entities)):
        t = eu_entities[i]
        # checks if the token of eu is the same as the last token of the extraction
        # = once the sentence is at the beginning of the IE
        if t.token == token[len(token) - 1]:
            j = i + 1
            while True:
                # break condition
                if t.pos_tag == konjunct_pos:
                    break
                try:
                    t = eu_entities[j]
                except IndexError:
                    return missing_part
                missing_part.append(t)
                j += 1

    return missing_part


def __combine_coordinates(conjuncts: list) -> list:
    """Determines the elliptic suffix in the last conjunct and appends it to all the other conjuncts.

            Parameters
            ----------
            conjuncts: list
                Receive a list with conjunct-modifier pairs.

            Returns
            -------
                list with compound conjuncts"""

    last_conjunct = conjuncts[len(conjuncts) - 1][1]
    last_conjunct = last_conjunct.replace(r'^[A-Za-zäÄüÜöÖß-]', "")
    # TODO Anwendung https://pypi.org/project/compound-split/
