"""Script to load resources files."""

# ## Imports
import codecs
import configuration
import logger
from information_extraction.models import Pattern, PatternToken, MatchedEntity, Modifier
from information_extraction.prepare_resources import convert_entities


# ## Functions

def read_known_entities(extraction_type: str) -> dict:
    # set variables
    entities = dict()
    switch = {
        "COMPETENCES": configuration.config_obj.get_competences_path(),
        "TOOLS": configuration.config_obj.get_tool_path(),
    }

    path = switch.get(extraction_type)

    logger.log_ie.info(f'Read entities from file: ' + path)

    try:
        f = codecs.open(path, "r", encoding="utf-8")

        while True:
            # read next line
            line = f.readline()

            # if line is empty, you are done with all lines in the file
            if not line:
                break

            # make line usable for normalization
            line = line.lower()
            # if there are more than one string in line, add strings to list
            entity = line.split(" ")
            # normalize strings of line
            for e in entity:
                index = entity.index(e)
                entity[index] = convert_entities.normalize_entities(e)

            # set found entities as MatchedEntities if there are known
            # if entity is not empty set as MatchedEntity
            if entity[0]:
                ie = MatchedEntity(start_lemma=entity[0], is_single_word=len(entity) == 1,
                                   ie_type=extraction_type, label=set())
                if not ie.is_single_word:
                    ie.set_lemma_array(entity)
                    entity = ' '.join(entity).strip()
                    ie.set_full_expression(entity)
                entities[hash(entity[0])] = ie
                continue
            else:
                continue

        # close file
        f.close()

    except FileNotFoundError:
        print(f'File not found.')
        logger.log_ie.info(f'Can not find File from ' + path + '.')

    return entities


def read_modifier() -> dict:
    # set variables
    entities = dict()
    path = configuration.config_obj.get_modifier_path()

    logger.log_ie.info(f'Read entities from file: ' + path)

    # get file object
    try:
        f = codecs.open(path, "r", encoding="utf-8")

        while True:
            # read next line
            line = f.readline()

            # if line is empty, you are done with all lines in the file
            if not line:
                break

            # make line usable for normalization
            line = line.lower()
            # if there are more than one string in line, add strings to list
            entity = line.split(" ")
            # normalize strings of line
            for e in entity:
                index = entity.index(e)
                entity[index] = convert_entities.normalize_entities(e)
            if entity[0]:
                modifier = Modifier(start_lemma=entity[0], is_single_word=len(entity) == 1)
                if not modifier.is_single_word:
                    modifier.set_lemma_array(entity)
                entities[hash(entity[0])] = modifier
                continue
            else:
                continue

        # close file
        f.close()

    except FileNotFoundError:
        print(f'File not found.')
        logger.log_ie.info(f'Can not find File from ' + path + '.')

    return entities


def read_failures(extraction_type: str) -> dict:
    """Creates a connection to the requested file and reads its contents.

            Parameters:
            ----------
                type: str
                    Receives a string that descripes the requested file. Options are shown in switch

            Returns:
            -------
                list
                    list with content from file"""

    # set variables
    entities = dict()
    switch = {
        "no_competences": configuration.config_obj.get_no_competences_path(),
        "no_tools": configuration.config_obj.get_no_tools_path(),
    }

    path = switch.get(extraction_type)

    logger.log_ie.info(f'Read entities from file: ' + path)

    # get file object
    try:
        f = codecs.open(path, "r", encoding="utf-8")

        while True:
            # read next line
            line = f.readline()

            # if line is empty, you are done with all lines in the file
            if not line:
                break

            # make line usable for normalization
            line = line.lower()
            # if there are more than one string in line, add strings to list
            entity = line.split(" ")
            # normalize strings of line
            for e in entity:
                index = entity.index(e)
                entity[index] = convert_entities.normalize_entities(e)
            # if return is empty, go to next line
            if entity[0]:
                # add line to list without spaces
                entities[hash(entity[0])] = entity
                continue
            else:
                continue

        # close file
        f.close()

    except FileNotFoundError:
        print(f'File not found.')
        logger.log_ie.info(f'Can not find File from ' + path + '.')

    return entities


def read_pattern_from_file(pattern_type: str) -> 'list[Pattern]':
    """Creates a connection to the requested file and reads its contents.

                Parameters:
                ----------
                    type: str
                        Receives a string that descripes the requested file. Options are shown in switch

                Returns:
                -------
                    list
                        list with pattern from file"""

    # set variables
    pattern_list = list()
    switch = {
        "comp_pattern": configuration.config_obj.get_comppattern_path(),
        "tool_pattern": configuration.config_obj.get_toolpattern_path(),
    }

    path = switch.get(pattern_type)

    logger.log_ie.info(f'Read pattern from file: ' + path)

    # get file object
    try:
        f = codecs.open(path, "r", encoding="utf-8")

        # set variables
        line_number = 0  # number of current line
        id = int()  # pattern id
        description = str()  # pattern description
        token_list = list()  # list with pattern token
        extraction_pointer = list()  # list with numbers of the tokens to be extracted

        while True:
            # read next line
            line = f.readline()

            # if line is empty, you are done with all lines in the file
            if not line:
                break

            line_number += 1
            pattern_content = line.split("\t")

            # check content from line
            try:
                if line.startswith("ID:"):
                    id = int(pattern_content[1].strip())

                if line.startswith("NAME:"):
                    description = pattern_content[1].strip()

                if line.startswith("TOKEN:"):
                    first_string = pattern_content[1]
                    if first_string == "null":
                        first_string = None
                    lemma = pattern_content[2]
                    if lemma == "null":
                        lemma = None
                    pos_tag = pattern_content[3]
                    if pos_tag == "null":
                        pos_tag = None
                    ie_token_str = pattern_content[4]
                    ie_token = bool()
                    if ie_token_str.__contains__("false"):
                        ie_token = False
                    elif ie_token_str.__contains__("true"):
                        ie_token = True
                    token = PatternToken(token=first_string, lemma=lemma, pos_tag=pos_tag, ie_token=ie_token)
                    if lemma and lemma.upper() == "IMPORTANCE":
                        token.modifier_token = True
                    token_list.append(token)

                if line.startswith("EXTRACT:"):
                    pointer = list()
                    ints = pattern_content[1].split(",")
                    for i in ints:
                        pointer.append(int(i))
                    extraction_pointer.extend(pointer)
                    # store variables as Pattern object
                    pattern = Pattern(id=id, description=description, pattern_token=token_list,
                                      extraction_pointer=extraction_pointer)
                    pattern_list.append(pattern)
                    token_list = list()
                    extraction_pointer = list()

            except Exception:
                print("Error in pattern file (line" + str(line_number) + ")")

        # close file
        f.close()

    except FileNotFoundError:
        print(f'File not found.')
        logger.log_ie.info(f'Can not find File from ' + path + '.')

    return pattern_list


def read_compounds(comp_type: str) -> dict:
    # set variables
    compounds = dict()
    switch = {
        'pos': configuration.config_obj.get_pos_comps_path(),
        'split': configuration.config_obj.get_split_comps_path(),
    }

    path = switch.get(comp_type)

    logger.log_ie.info(f'Read entities from file: ' + path)

    try:
        f = codecs.open(path, "r", encoding="utf-8")

        while True:
            # read next line
            line = f.readline()

            # if line is empty, you are done with all lines in the file
            if not line:
                break

            # separated line by character
            parts = line.split('\\|')
            if len(parts) > 1:
                compounds[hash(parts[0] + parts[1])] = parts

        # close file
        f.close()

    except FileNotFoundError:
        print(f'File not found.')
        logger.log_ie.info(f'Can not find File from ' + path + '.')

    return compounds
