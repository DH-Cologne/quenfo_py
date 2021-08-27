import re
import sys

def gen_classes(para, regex_clf):

    def f(x, y):
        test = re.match(y, para.lower())
        # captures saves multiple matches if more than one found
        try:
            test.captures(1)
        except AttributeError:
            pass
        
        if test is not None:
            return (x, test)

    result = [f(x, y) for x, y in zip(regex_clf['class_nr'], regex_clf['pattern'])]
    result = list(filter(None, result))

    return result