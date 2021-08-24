# ## Open Configuration-file and set paths to txt files with lists, pattern etc.
import codecs

# load config file
from pathlib import Path

import yaml

from information_extraction.prepare_resources import convert_entities

# ## Open Configuration-file and set paths to models (trained and retrained)
with open(Path(r'C:\Users\Christine\Documents\Qualifikationsentwicklungsforschung\quenfo\quenfo_py\code\config.yaml'),
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
    pattern = list()
    switch = {
        "comp_pattern": comppattern_path,
        "tool_pattern": toolpattern_path,
    }

    path = switch.get(type)

    return pattern
