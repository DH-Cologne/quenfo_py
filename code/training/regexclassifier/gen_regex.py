import pandas as pd
from pathlib import Path
def start(regex_path: str) -> pd.DataFrame():

    regex_clf = pd.DataFrame()
    class_list = list()
    pattern_list = list()

    with open(Path(regex_path), 'rb') as f:
        for line in f.readlines():
            line = [x for x in (line.decode()).split('\t')]
            if not(line[0].__contains__('#')):
                class_list.append(line[0])
                pattern_list.append(line[1].replace("\r\n", ""))
            else:
                continue
        f.close()

    regex_clf['class_nr'] = class_list
    regex_clf['pattern'] = pattern_list

    return regex_clf