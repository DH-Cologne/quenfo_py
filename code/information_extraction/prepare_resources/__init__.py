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
