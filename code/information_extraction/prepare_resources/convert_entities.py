def normalize_entities_from_file(entity: str) -> str:
    """Normalizes the given string - trim - deletes (most) special characters at the begin and end of the string
        (with some exceptions)

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
        if len(entity) <= 1:
            return entity
    if entity == "--":
        return entity

    while True:
        entity = entity.strip()
        if len(entity) == 0:
            break
        # check first character of given string
        first_character = entity[0]
        if first_character == "_":
            # remove character
            entity = entity[1:len(entity)].strip()
        if len(entity) == 0:
            break
        # check if first character is not a letter, a digit or special character and remove character
        if not (first_character.isalpha() and first_character.isdigit() and first_character == "§"):
            entity = entity[1:len(entity)].strip()
        else:
            break
        if len(entity) == 0:
            break

    while True:
        if len(entity) == 0:
            break
        # check last character of given string
        last_character = entity[len(entity) - 1]
        if last_character == "_":
            # remove character
            entity = entity[0:len(entity) - 1].strip()
        # check if first character is not a letter, a digit or special character and remove character
        if not (last_character.isalpha() and last_character.isdigit() and last_character == "+"
                and last_character == "#"):
            entity = entity[0:len(entity) - 1].strip()
        else:
            break

    return entity
