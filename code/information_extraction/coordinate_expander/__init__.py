# ##Imports
from compound_split.char_split import split_compound
import logger
from information_extraction.helper import is_all_upper
from information_extraction.models import Token
from information_extraction.prepare_extractionunits.convert_extractionunits import get_lemmata

# set variables
poss_resolvation = dict()


# ##Functions
def resolve(complete_entity, eu_entities, debug: bool) -> list:
    """Resolves all coordinations in the expression and returns a list of tokens for each resolution.
    Feature of a coordination here is a conjunction.

            Parameters
            ----------
                complete_entity
                    Receives a list with all TextToken of extraction.
                eu_entities
                    Receives a list with all TextToken of ExtractionUnit.
                debug
                    Information about Debugging.

            Returns
            -------
                list of lemmas for every resolved coordination"""

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
    else:
        kon_index = pos_tags.index('KON')
        if token[kon_index + 1].startswith('-'):
            return __resolve_left_ellipsis(token, pos_tags, lemmata, eu_entities, debug)

        empty_return = list()
        return empty_return


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
    if end_koo < 0:  # if coordination is cut off
        missing_part = __complete_coordinate(eu_entities, token, konjunct_pos)
        for t in missing_part:
            token.append(t.token)
            pos_tags.append(t.pos_tag)
            lemmata.append(t.lemma)

        end_koo = len(token) - 1
    else:
        end_koo = end_koo + start_koo  # because of subList index

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
    coordinates = __combine_coordinates_r(conjuncts)

    # return resolution to remaining block
    for c in coordinates:
        combined_token = list()
        combined = list()
        combined.append('<root>')
        combined.extend(before)
        if c[0] is not None:
            adja = c[0].replace(r'[^A-Za-zäÄüÜöÖß\\s-]', '')
            combined.append(adja.strip())
        combined.append(c[1].replace(r'[^A-Za-zäÄüÜöÖß-]', ''))
        combined.extend(after)

        # lemmatize resolved sentence
        resolved_lemmata = list()
        for token in combined:
            lemma = get_lemmata(token)
            resolved_lemmata.append(lemma)

        if len(resolved_lemmata) == 2:  # if IE consists of only one lemma (+root)
            right_lemma = lemmata[end_koo].replace(r'[^A-Za-zäÄüÜöÖß-]', '')
            # check if compound token was lemmatized correctly
            resolved_lemma = resolved_lemmata[len(before) + 1]
            if not resolved_lemma[len(resolved_lemma) - 1] == right_lemma[len(right_lemma) - 1]:
                resolved_lemmata[len(before) + 1] = __correct_lemma(resolved_lemma, right_lemma)

        for i, item in enumerate(resolved_lemmata, start=1):
            tt = Token(token=combined[i], lemma=resolved_lemmata[i], pos_tag=None)  # TODO pos
            combined_token.append(tt)

        if debug:
            print(str(combined_token))

        resolved_token.append(combined_token)

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


def __combine_coordinates_r(conjuncts: list) -> list:
    """Determines the elliptic suffix in the last conjunct and appends it to all the other conjuncts.

            Parameters
            ----------
            conjuncts: list
                Receive a list with conjunct-modifier pairs.

            Returns
            -------
                list with compound conjuncts"""

    # set globals
    global poss_resolvation

    last_conjunct = conjuncts[len(conjuncts) - 1][1]
    last_conjunct = last_conjunct.replace(r'[^A-Za-zäÄüÜöÖß-]', "")
    # division into morphemes
    subtoken = split_compound(last_conjunct)
    subtoken = subtoken[0][1: len(subtoken)]

    compound = ''  # morpheme (composita) to be attached to each ellipsis

    if len(subtoken) == 1:  # if compound splitter has not found a separation
        # methods to find a separation yourself
        compound = subtoken[0]
        if compound.__contains__('-'):
            splits = compound.split('-')
            if len(splits) == 2:
                compound = splits[1]
                poss_resolvation[splits[0]] = splits[1]
            else:  # more than one hyphen
                first_morphem = splits[0]
                compound = last_conjunct.replace(first_morphem + '-', '')
                poss_resolvation[first_morphem] = compound
        else:  # TODO own composite design
            poss_resolvation[subtoken[0]] = ''
            compound = subtoken[0]

    elif len(subtoken) == 2:  # if exactly two morphemes are found, the latter is chosen
        compound = subtoken[1]

    else:  # splitter has found more than two morphemes
        compound = subtoken[len(subtoken) - 1]
        poss_resolvation[last_conjunct.replace(compound, '')] = compound

    for i in range(len(conjuncts)):
        ellipse = conjuncts[i][1]
        # cases where the complementary dash must remain as a hyphen (PC- // MS-Office- // ...)
        ellipse_is_upper = is_all_upper(ellipse)

        if not compound == '':
            if ellipse_is_upper:
                # keep hyphen, capitalize compound
                compound = compound[0].upper() + compound[1: len(compound)]
            else:
                ellipse = ellipse.replace('-', '')

        conjuncts[i][1] = ellipse + compound

    return conjuncts


def __correct_lemma(wrong_lemma: str, right_lemma: str) -> str:
    """Matches the suffix of the wrong lemma to the suffix of the correct lemma.

            Parameters
            ----------
                wrong_lemma: str
                    Receives a string with a lemma to be aligned
                right_lemma
                    Receives a string with a lemma to be aligned to
            Returns
            -------
                string with aligned lemma"""

    # find matching substring
    # assumption: suffix of rightLemma is correct in any case, wrongLemma is too short or too long
    i = wrong_lemma.rindex(right_lemma[len(right_lemma) - 1])
    suffix = ''

    if i < 0:  # suffix of the right lemma is not in the wrong lemma -> wrongLemma too short
        i = len(right_lemma) - 1
        try:
            while True:
                if right_lemma[i] == wrong_lemma[len(wrong_lemma) - 1]:
                    break
                suffix = right_lemma[i] + suffix
                i -= 1
        except IndexError:
            return wrong_lemma  # happens when pos was not awarded properly

        wrong_lemma = wrong_lemma + suffix

    else:  # wrongLemma too long
        wrong_lemma = wrong_lemma[0: i + 1]

    return wrong_lemma


def __resolve_left_ellipsis(token: list, pos_tags: list, lemmata: list, eu_entities: list, debug: bool) -> list:
    """Resolves left coordinations in the expression and returns a list of tokens for each resolution.

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
    end_koo = len(token) - 1
    while not token[end_koo].startswith('-'):
        end_koo -= 1
    conjunct_pos = pos_tags[end_koo]
    start_koo = end_koo - 1     # pos as with all the others?
    while True:
        if not token[start_koo].startswith('-') and pos_tags[start_koo] == conjunct_pos:
            break
        start_koo -= 1

    # tokens that are in front of the coordination
    before = list()
    for i in range(start_koo):
        before.append(token[i])

    # tokens that stand after the coordination
    after = list()
    for i, item in enumerate(token, start=end_koo + 1):
        after.append(token[i])

    pos_to_ignore = list()
    pos_to_ignore.append('KON')
    pos_to_ignore.append('$,')
    conjuncts = list()
    for i in range(start_koo, end_koo):
        if not pos_to_ignore.__contains__(pos_tags[i]):
            conjuncts.append(token[i])

    coordinates = __combine_coordinates_l(conjuncts)
    # return resolution to remaining block
    for c in coordinates:
        combined = list()
        combined_token = list()
        if not before.__contains__('<root>'):
            combined.append('<root>')

        combined.extend(before)
        combined.append(c.replace(r'[^A-Za-zäÄüÜöÖß-]', ''))
        combined.extend(after)

        # lemmatize resulted sentence
        resolved_lemmata = list()
        for token in combined:
            lemma = get_lemmata(token)
            resolved_lemmata.append(lemma)

        for i, item in enumerate(resolved_lemmata, start=1):
            combined_token.append(Token(token=combined[i], lemma=resolved_lemmata[i], pos_tag=None))

        resolved_token.append(combined_token)

    return resolved_token


def __combine_coordinates_l(conjuncts: list) -> list:
    """Determines the elliptic suffix in the first conjunct and appends it to all the other conjuncts.

                Parameters
                ----------
                conjuncts: list
                    Receive a list with conjunct-modifier pairs.

                Returns
                -------
                    list with compound conjuncts"""

    # set globals
    global poss_resolvation

    first_conjunct = conjuncts[0]
    first_conjunct = first_conjunct.replace(r'[^A-Za-zäÄüÜöÖß-]', '')

    # division into morphemes
    subtoken = split_compound(first_conjunct)
    subtoken = subtoken[0][1: len(subtoken)]

    compound = ''  # morpheme(composita) to be attached to each ellipsis
    if len(subtoken) == 1:  # if compound splitter has not found a separation
        # methods to find a separation yourself
        compound = subtoken[0]
        if compound.__contains__('-'):
            splits = compound.split('-')
            if len(splits) == 2:
                compound = splits[0]
                poss_resolvation[splits[0]] = splits[1]
            else:  # more than one hyphen
                first_morphem = splits[0]
                compound = first_conjunct.replace(first_morphem + '-', '')
                poss_resolvation[first_morphem] = compound

        else:
            poss_resolvation[subtoken[0]] = ''
            compound = subtoken[0]

    elif len(subtoken) == 2:  # if exactly two morphemes are found, the latter is chosen
        compound = subtoken[0]

    else:  # splitter has found more than two morphemes
        compound = subtoken[0]
        poss_resolvation[first_conjunct.replace(compound, '')] = compound

    for i, item in enumerate(conjuncts, start=1):
        ellipse = conjuncts[i]
        if not compound == '':
            # if ellipse starts capitalized, hyphen is kept
            if ellipse[1].islower():
                ellipse = ellipse.replace('-', '')
        conjuncts[i] = compound + ellipse

    return conjuncts
