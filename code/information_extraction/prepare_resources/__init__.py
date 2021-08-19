from information_extraction.prepare_resources import connection_resources

competences = connection_resources.get_entities_from_file("competences")
no_competences = connection_resources.get_entities_from_file("no_competences")
modifier = connection_resources.get_entities_from_file("modifier")
tools = connection_resources.get_entities_from_file("tools")
no_tools = connection_resources.get_entities_from_file("no_tools")
