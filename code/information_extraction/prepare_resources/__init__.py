"""Script to load list with known entities, extraction fails, modifiers and pattern from resource files."""

# ## Imports
from information_extraction.models import Pattern
from information_extraction.prepare_resources import connection_resources

# ## Set variables
competences = dict()
no_competences = dict()
modifier = dict()
comp_pattern = list()
tools = dict()
no_tools = dict()
tool_pattern = list()

possible_comppounds = dict()
splitted_compounds = dict()


# ## Functions
def set_ie_resources() -> None:
    """Function to load files from resources.

            Returns:
            -------
                None"""

    # set globals
    global competences, no_competences, modifier, comp_pattern, tools, no_tools, tool_pattern, possible_comppounds, \
        splitted_compounds

    # fill variables with content
    # variables for competences
    competences = connection_resources.read_known_entities('COMPETENCES')
    no_competences = connection_resources.read_failures('no_competences')
    modifier = connection_resources.read_modifier()
    comp_pattern = connection_resources.read_pattern_from_file('comp_pattern')

    # variables for tools
    tools = connection_resources.read_known_entities('TOOLS')
    no_tools = connection_resources.read_failures('no_tools')
    tool_pattern = connection_resources.read_pattern_from_file('tool_pattern')

    # variables for compounds
    possible_comppounds = connection_resources.read_compounds('pos')
    splitted_compounds = connection_resources.read_compounds('split')


# Getter
def get_ie_pattern(ie_mode: str) -> 'list[Pattern]':
    if ie_mode == 'TOOLS':
        return tool_pattern
    elif ie_mode == 'COMPETENCES':
        return comp_pattern
    elif ie_mode == 'COMPETENCES AND TOOLS':
        all_pattern = list()
        all_pattern.extend(comp_pattern)
        all_pattern.extend(tool_pattern)
        return all_pattern


def get_entities(ie_mode: str) -> dict:
    if ie_mode == 'TOOLS':
        return tools
    elif ie_mode == 'COMPETENCES':
        return competences
    elif ie_mode == 'COMPETENCES AND TOOLS':
        all_entities = dict(list(competences.items()) + list(tools.items()))
        return all_entities


def get_no_entities(ie_mode: str) -> dict:
    if ie_mode == 'TOOLS':
        return no_tools
    elif ie_mode == 'COMPETENCES':
        return no_competences
    elif ie_mode == 'COMPETENCES AND TOOLS':
        all_entities = dict(list(no_competences.items()) + list(no_tools.items()))
        return all_entities


def get_modifier() -> dict:
    return modifier


def get_compounds(comp_type: str) -> dict:
    if comp_type == 'pos':
        return possible_comppounds
    elif comp_type == 'split':
        return splitted_compounds
    elif comp_type == 'all':
        all_compounds = dict(list(possible_comppounds.items()) + list(splitted_compounds.items()))
        return all_compounds
