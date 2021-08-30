import re

def gen_classes(para, regex_clf):

    def __compare_matches(class_nr, pattern):
        # check if pattern is in para
        match_result = re.match(pattern, para.lower())
        # captures() saves multiple matches if more than one is found
        try:
            match_result.captures(1)
        except AttributeError:
            pass
        
        if match_result is not None:
            return (class_nr, match_result)

    result = [__compare_matches(class_nr, pattern) for class_nr, pattern in zip(regex_clf['class_nr'], regex_clf['pattern'])]
    # remove duplicates
    result = list(filter(None, result))
    # return list of matches with associated classes
    return result