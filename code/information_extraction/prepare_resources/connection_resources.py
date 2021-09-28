# ## Open Configuration-file and set paths to txt files with lists, pattern etc.
import codecs

import configuration
import logger
from information_extraction.models import Pattern, PatternToken, MatchedEntity, Modifier
from information_extraction.prepare_resources import convert_entities


def get_entities_from_file(extraction_type: str) -> list:
    """Creates a connection to the requested file and reads its contents.

        Parameters:
        ----------
            type: str
                Receives a string that descripes the requested file. Options are shown in switch

        Returns:
        -------
            list
                list with content from file"""
    entities = list()
    switch = {
        "COMPETENCES": configuration.config_obj.get_competences_path(),
        "no_competences": configuration.config_obj.get_no_competences_path(),
        "modifier": configuration.config_obj.get_modifier_path(),
        "TOOLS": configuration.config_obj.get_tool_path(),
        "no_tools": configuration.config_obj.get_no_tools_path(),
    }

    path = switch.get(extraction_type)

    logger.log_ie.info(f'Read entities from file: ' + path)

    # get file object
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
        if extraction_type == "COMPETENCES" or extraction_type == "TOOLS":
            # if entity is not empty set as MatchedEntity
            if entity[0]:
                ie = MatchedEntity(start_lemma=entity[0], is_single_word=len(entity) == 1, ie_type=extraction_type,
                                   label=set())
                if not ie.is_single_word:
                    ie.set_lemma_array(entity)
                    entity = ' '.join(entity).strip()
                    ie.set_full_expression(entity)
                entities.append(ie)
                continue
            else:
                continue
        elif extraction_type == 'modifier':
            if entity[0]:
                modifier = Modifier(start_lemma=entity[0], is_single_word=len(entity) == 1)
                if not modifier.is_single_word:
                    modifier.set_lemma_array(entity)
                entities.append(modifier)
                continue
            else:
                continue
        # otherwise (no_tools or no_comptenteces) set one line to one string
        else:
            # if return is not empty, join strings from list
            normalize_entity = " ".join(entity).strip()
            # if return is empty, go to next line
            if normalize_entity:
                # add line to list without spaces
                entities.append(normalize_entity)
                continue
            else:
                continue

    # close file
    f.close()

    return entities


def read_pattern_from_file(pattern_type: str) -> 'list[Pattern]':
    pattern_list = list()
    switch = {
        "comp_pattern": configuration.config_obj.get_comppattern_path(),
        "tool_pattern": configuration.config_obj.get_toolpattern_path(),
    }

    path = switch.get(pattern_type)

    logger.log_ie.info(f'Read pattern from file: ' + path)

    f = codecs.open(path, "r", encoding="utf-8")

    line_number = 0
    id = int()
    description = str()
    token_list = list()
    extraction_pointer = list()

    while True:
        # read next line
        line = f.readline()

        # if line is empty, you are done with all lines in the file
        if not line:
            break

        line_number += 1
        pattern_content = line.split("\t")

        try:
            if line.startswith("ID:"):
                id = int(pattern_content[1].strip())
            if line.startswith("NAME:"):
                description = pattern_content[1].strip()
            if line.startswith("TOKEN:"):
                first_string = pattern_content[1]
                if first_string.__eq__("null"):
                    first_string = None
                lemma = pattern_content[2]
                if lemma.__eq__("null"):
                    lemma = None
                pos_tag = pattern_content[3]
                if pos_tag.__eq__("null"):
                    pos_tag = None
                ie_token_str = pattern_content[4]
                ie_token = bool()
                if ie_token_str.__contains__("false"):
                    ie_token = False
                elif ie_token_str.__contains__("true"):
                    ie_token = True
                token = PatternToken(token=first_string, lemma=lemma, pos_tag=pos_tag, ie_token=ie_token)
                if lemma and lemma.upper().__eq__("IMPORTANCE"):
                    token.modifier_token = True
                token_list.append(token)
            if line.startswith("EXTRACT:"):
                pointer = list()
                ints = pattern_content[1].split(",")
                for i in ints:
                    pointer.append(int(i))
                extraction_pointer.extend(pointer)
                pattern = Pattern(id=id, description=description, pattern_token=token_list,
                                  extraction_pointer=extraction_pointer)
                pattern_list.append(pattern)
                token_list = list()
                extraction_pointer = list()

        except Exception:
            print("Error in pattern file (line" + str(line_number) + ")")

    f.close()

    return pattern_list
