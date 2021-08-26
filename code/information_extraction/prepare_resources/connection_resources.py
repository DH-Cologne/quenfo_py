# ## Open Configuration-file and set paths to txt files with lists, pattern etc.
import codecs

# load config file
from pathlib import Path

import yaml

from information_extraction.models import Pattern, PatternToken
from information_extraction.prepare_resources import convert_entities

# ## Open Configuration-file and set paths to models (trained and retrained)
with open(Path(r'C:\Users\krist\Documents\Qualifikationsentwicklungsforschung\quenfo_py\code\config.yaml'),
          'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)

# get path from config
# competences
competence_path = cfg['resources']['competences_path']
no_competence_path = cfg['resources']['nocompetences_path']
modifier_path = cfg['resources']['modifier_path']
comppattern_path = cfg['resources']['comppattern_path']

# tools
tools_path = cfg['resources']['tools_path']
no_tools_path = cfg['resources']['notools_path']
toolpattern_path = cfg['resources']['toolpattern_path']


def get_entities_from_file(type: str) -> list:
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
        "competences": competence_path,
        "no_competences": no_competence_path,
        "modifier": modifier_path,
        "tools": tools_path,
        "no_tools": no_tools_path,
    }

    path = switch.get(type)

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


def read_pattern_from_file(type: str) -> list:
    pattern_list = list()
    switch = {
        "comp_pattern": comppattern_path,
        "tool_pattern": toolpattern_path,
    }

    path = switch.get(type)

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
