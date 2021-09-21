# Imports
import pandas as pd
import sqlite3
from sqlite3 import Error

# Paths definieren
input_path = '..\\..\\quenfo_data\\resources\\classification\\trainingSets\\trainingdata_anonymized.tsv'
output_path = '..\\..\\quenfo_v1_1_3\\quenfo_data\\sqlite\\orm\\traindata_sql.db'


# Loads Input Data (Trainingdata) and readlines
def load_input_data():
    # create a database connection
    with open(input_path, 'r', encoding="utf-8") as f:
        filelines = f.readlines()
    return filelines


# Gets filelines and transfers content to dataframe
def transfer_lines_to_df(filelines):
    postingID = str
    classID = 0
    line_content = []
    all_rows = []

    for line in filelines:
        # If line is divided by 2 or 3 tabs, it is the header (with the important information): postingID, Zeilennr. und classID
        if line.split('\t').__len__() == 3 or line.split('\t').__len__() == 2:
            splitted = line.split('\t')
            classID = splitted[2] 
            postingID = splitted[0]
            zeilennr = splitted[1]
        # All other lines (that are not empty) are content-information
        elif line != '\n':
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
            # reset list
            list_df_prepraration= []
 
    # Generate df with all rows in specific columns
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
