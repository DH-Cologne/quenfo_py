from information_extraction.models import Configuration


def get_search_type() -> int:
    search_type = int()

    # standard value for tool extraction
    if "tool" in Configuration.ie_type:
        search_type = 6

    # get value from config for competence extraction
    elif "competences" in Configuration.ie_type and Configuration.search is not None:
        search_type = Configuration.search

    # default for competence extraction
    elif "competences" in Configuration.ie_type and Configuration.search is None:
        search_type = 3

    return search_type