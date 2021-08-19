# ## Open Configuration-file and set paths to txt files with lists, pattern etc.
import codecs
from pathlib import Path

import yaml

# load config file
from information_extraction.prepare_resources import convert_entities

with open(Path('config.yaml'), 'r') as yamlfile:
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

        # make line usable for normalization
        line = line.lower()
        entity = line.split(" ")

        # normalize first string of line
        keyword = convert_entities.normalize_entities_from_file(entity[0])
        if entity is None:
            line = f.readline()
            continue
        else:
            line = " ".join(entity)
        # if line is empty, you are done with all lines in the file
        if not line:
            break

        # add line to list
        entities.append(line)

    # close file
    f.close()

    return entities
