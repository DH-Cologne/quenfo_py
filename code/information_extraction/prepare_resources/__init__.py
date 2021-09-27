from information_extraction.models import Pattern
from information_extraction.prepare_resources import connection_resources

# ## Set Variables
competences = list()
no_competences = list()
modifier = list()
comp_pattern = list()
tools = list()
no_tools = list()
tool_pattern = list()


# ## Functions
# Load Resources
def set_ie_resources() -> None:
    global competences, no_competences, modifier, comp_pattern, tools, no_tools, tool_pattern

    competences = connection_resources.get_entities_from_file('competences')
    no_competences = connection_resources.get_entities_from_file('no_competences')
    modifier = connection_resources.get_entities_from_file('modifier')
    comp_pattern = connection_resources.read_pattern_from_file('comp_pattern')

    tools = connection_resources.get_entities_from_file('tools')
    no_tools = connection_resources.get_entities_from_file('no_tools')
    tool_pattern = connection_resources.read_pattern_from_file('tool_pattern')


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


def get_entities(ie_mode: str) -> list:
    if ie_mode == 'TOOLS':
        return tools
    elif ie_mode == 'COMPETENCES':
        return competences
    elif ie_mode == 'COMPETENCES AND TOOLS':
        all_entities = list()
        all_entities.extend(competences)
        all_entities.extend(tools)
        return all_entities


def get_no_entities(ie_mode: str) -> list:
    if ie_mode == 'TOOLS':
        return no_tools
    elif ie_mode == 'COMPETENCES':
        return no_competences
    elif ie_mode == 'COMPETENCES AND TOOLS':
        all_entities = list()
        all_entities.extend(no_competences)
        all_entities.extend(no_tools)
        return all_entities
