def normalize_entities(entity: str) -> str:
    """Normalizes the given string - trim - deletes (most) special characters at the begin and end of the string
        (with some exceptions).

        Parameters:
        -----------
            entity: str
                Receives string to normalize.

        Returns:
        -------
            str
                normalized string"""

    entity = entity.strip()
    # returns string without modifications
    if entity.startswith("<end-"):
        return entity
    if entity.startswith("<root-"):
        return entity
    if entity == "--":
        return entity

    while True:
        entity = entity.strip()
        if len(entity) == 0:
            break
        # check first character of given string
        first_character = entity[0]
        if first_character.__eq__("_"):
            entity = entity[1:len(entity)].strip()
        if len(entity) == 0:
            break
        # check if first character is not a letter, a digit or special character and remove character
        if not first_character.isalpha() and not first_character.isdigit() and not first_character.__eq__("§"):
            entity = entity[1:len(entity)].strip()
        else:
            break
        if len(entity) == 0:
            break
        break

    while True:
        if len(entity) == 0:
            break
        # check last character of given string
        last_character = entity[len(entity) - 1]
        if last_character.__eq__("_"):
            entity = entity[0:len(entity) - 1].strip()
        if len(entity) == 0:
            break
        # check if first character is not a letter, a digit or special character and remove character
        if not last_character.isalpha() and not last_character.isdigit() and not last_character.__eq__("+") and not last_character.__eq__("#"):
            entity = entity[0:len(entity) - 1].strip()
        else:
            break
        break

    return entity