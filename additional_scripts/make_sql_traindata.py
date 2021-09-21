# Imports
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
<<<<<<< HEAD:additional_scripts/make_sql_traindata.py
=======
    # print(filelines)
>>>>>>> 8556f489fb9eeb290f76787d221be24aebd2bf3b:make_sql_traindata.py
    return filelines


# Gets filelines and transfers content to dataframe
def transfer_lines_to_df(filelines):
    postingID = str
    classID = 0
    line_content = []
    all_rows = []

    for line in filelines:
<<<<<<< HEAD:additional_scripts/make_sql_traindata.py
        # If line is divided by 2 or 3 tabs, it is the header (with the important information): postingID, Zeilennr. und classID
        if line.split('\t').__len__() == 3 or line.split('\t').__len__() == 2:
            splitted = line.split('\t')
            classID = splitted[2] 
=======
        # Wenn eine Zeile 2 oder 3 Tabs hat, handelt es sich um die Kopfzeile mit den Informationen: postingID,
        # Zeilennr. und classID
        if line.split('\t').__len__() == 3 or line.split('\t').__len__() == 2:
            splitted = line.split('\t')
            # print(line)
            classID = splitted[2]
>>>>>>> 8556f489fb9eeb290f76787d221be24aebd2bf3b:make_sql_traindata.py
            postingID = splitted[0]
            zeilennr = splitted[1]
        # All other lines (that are not empty) are content-information
        elif line != '\n':
<<<<<<< HEAD:additional_scripts/make_sql_traindata.py
=======
            # print(line)
>>>>>>> 8556f489fb9eeb290f76787d221be24aebd2bf3b:make_sql_traindata.py
            line_content.append(line)
        # These are the empty lines that are used to subdivide the individual job advertisements
        else:
            # join lines to one content-text
            content = ''.join(line_content)
            # Reset line_content for each jobad
            line_content = []
            # Create an entry in the list with all the information you have collected for the current job
            list_df_prepraration = [postingID, zeilennr, classID, content]
            # Create an entry for the Jobad in a large list
            all_rows.append(list_df_prepraration)
<<<<<<< HEAD:additional_scripts/make_sql_traindata.py
            # reset list
            list_df_prepraration= []
 
    # Genearte df with all rows in specific columns
=======
            # Setze die Jobad liste zurück
            list_df_prepraration = []

    # Generiere das df mit den gesammelten Infos und folgenden Spalten:
>>>>>>> 8556f489fb9eeb290f76787d221be24aebd2bf3b:make_sql_traindata.py
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

<<<<<<< HEAD:additional_scripts/make_sql_traindata.py
# Main Method
=======

# Main Methode
>>>>>>> 8556f489fb9eeb290f76787d221be24aebd2bf3b:make_sql_traindata.py
def main():
    filelines = load_input_data()
    df = transfer_lines_to_df(filelines)
    writer(df)


if __name__ == "__main__":
    main()
