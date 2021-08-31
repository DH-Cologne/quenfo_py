import re

def gen_classes(para, regex_clf):
    result = list()

    def __compare_matches(class_nr, pattern):
        # check if pattern is in para
        match_result = re.match(pattern, para.lower())
        # captures() saves multiple matches if more than one is found
        try:
            match_result.captures(1)
        except AttributeError:
            pass
        #print(match_result)
        if match_result == None:
            return None
        else:
            return int(class_nr)

    result = [__compare_matches(class_nr, pattern) for class_nr, pattern in zip(regex_clf['class_nr'], regex_clf['pattern'])]
    # remove None from list
    result = list(filter(None, result))
    # remove duplicates from list
    result = list(dict.fromkeys(result))

    # return list of matches with associated classes
    return result


