import pandas as pd
import sqlite3
from sqlite3 import Error
import os

# Paths definieren
input_path = 'C:\\Users\\Christine\\Documents\\Qualifikationsentwicklungsforschung\\quenfo\\quenfo_v1_1_3\\quenfo_data\\resources\\classification\\trainingSets\\trainingdata_anonymized.tsv'
output_path = 'C:\\Users\\Christine\\Documents\\Qualifikationsentwicklungsforschung\\quenfo\\quenfo_v1_1_3\\quenfo_data\\sqlite\\orm\\traindata_sql.db'


# Loads Input Data (Trainingdata) and readlines
def load_input_data():
    # create a database connection
    with open(input_path, 'r', encoding="utf-8") as f:
        filelines = f.readlines()
    # print(filelines)
    return filelines


# Gets filelines and transfers content to dataframe
def transfer_lines_to_df(filelines):
    jahrgang = 0
    postingID = str
    classID = 0
    line_content = []
    all_rows = []

    for line in filelines:
        # Wenn eine Zeile 2 oder 3 Tabs hat, handelt es sich um die Kopfzeile mit den Informationen: postingID,
        # Zeilennr. und classID
        if line.split('\t').__len__() == 3 or line.split('\t').__len__() == 2:
            splitted = line.split('\t')
            # print(line)
            classID = splitted[2]
            postingID = splitted[0]
            zeilennr = splitted[1]
        # Alle anderen Zeilen, die keine leeren Zeilen sind, sind content-Informationen
        elif line != '\n':
            # print(line)
            line_content.append(line)
        # Das sind die leeren Zeilen, die zur Unterteilung zwischen den einzelnen Stellenanzeigen benutzt werden
        else:
            # Füge die einzelnen Content-Sätze zu einem Text zsm
            content = ''.join(line_content)
            # Setze line_content für die nächste Jobad zurück
            line_content = []
            # Erstelle mit allen gesammelten Infos für die aktuelle Jobad einen Eintrag in der Liste
            list_df_prepraration = [postingID, zeilennr, classID, content]
            # Lege Eintrag für die Jobad in großer Liste an
            all_rows.append(list_df_prepraration)
            # Setze die Jobad liste zurück
            list_df_prepraration = []

    # Generiere das df mit den gesammelten Infos und folgenden Spalten:
    df = pd.DataFrame(all_rows, columns=['postingId', 'zeilennr', 'classID', 'content'])
    return df


# Gets dataframe and stores it in new sqlite database
def writer(df_train):
    conn_temp = None

    # Name of database table
    key = 'traindata'

    df_train['index'] = df_train.index

    # make connection
    try:
        conn_temp = sqlite3.connect(output_path)
    except Error as e:
        print(e)

    # create filler table or else pass
    try:
        conn_temp.execute('''CREATE TABLE {}
                            ([Client_Name] text, [Country_Name] text, [Date] date)'''.format(key))
        conn_temp.commit()
    except:
        pass

    # get filler content and overwrite with dataframe content
    data = pd.read_sql('SELECT * FROM {}'.format(key), conn_temp)
    data = df_train
    data.to_sql(key, conn_temp, if_exists='replace', chunksize=1000, index=False)
    conn_temp.close()


# Main Methode
def main():
    filelines = load_input_data()
    df = transfer_lines_to_df(filelines)
    writer(df)


if __name__ == "__main__":
    main()
