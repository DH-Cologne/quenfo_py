# ## Imports
import sqlalchemy
from classification.prepare_classifyunits import generate_classifyunits
from database import session, session2
from orm_handling import orm
from orm_handling.models import ClassifyUnits
from database import engine
import logging
import sys
import yaml
from pathlib import Path
from classification import predict_classes
import datetime
import os 
import time

# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    resources = cfg['resources']
    traindata_path = resources['traindata_path']

# hier wird eigentlich das model übergeben
def classify(model):
    # ## STEP 1:
    # Load the Input data: JobAds in JobAds Class.
    jobads = orm.get_jobads(session)

    #generate classify_units, feature_units for Testdata
    for jobad in jobads:
        # ## TODO: PREPARE CLASSIFY UNITS
        # Pass list of JobAds-objects to be converted to clean paragraphs, featureunits and feature vectors
        generate_classifyunits(jobad, model)
        # add obj to current session --> to be written in db
        orm.create_output(session, jobad)
    
    for jobad in jobads:

        predict_classes.start_prediction(jobad, model)
        orm.create_output(session, jobad)


    # Commit generated classify units with paragraphs and class assignments to table
    orm.pass_output(session)
    try:
        orm.delete_filler(session2)
        # Das hier bedeutet, dass trainiert wurde! das heißt auch, dass das model bereits über den aktuellen stamp verfügt. 
        # Die Trainingsdaten schließen aber erst hier, weshalb die zeit leicht unterschiedlich ist. Deshalb soll, wenn neu trainiert wurde, der Timestamp
        # für tfidf und auch für knn neu gesetzt werden!

        # also hier an der stelle muss beides neu trainiert worden sein. Abgleich ob beide auch die gleichen trainingsdaten bekommen haben:
        #if model.vectorizer.input == model.model_knn.input:
        #actual_timestamp = (model.vectorizer.input).split('$')[1]

        # HIER NOCH EINE EXCEPTION HIN, wenn aus dem pfad nich die namen entnommen werden können
        actual_date = model.traindata_date
        print(actual_date)
        try:
            overwrite_file = Path(traindata_path)
            splitter = actual_date.split(' ')
            datum = splitter[0].split('-')
            year = datum[0]
            month = datum[1]
            day = datum[2]
            kleinerezeit = splitter[1].split(':')
            hour = kleinerezeit[0]
            minute = kleinerezeit[1]
            second = kleinerezeit[2]
        except IndexError:
            hour = 00
            minute = 00
            second = 00

        date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second), microsecond=0)
        modTime = time.mktime(date.timetuple())
        os.utime(overwrite_file, (modTime, modTime))

    except sqlalchemy.exc.OperationalError as err:
        print(f'{err}: No need to delete traindata-filler because traindata didnt get processed (model was already there)')
    session.close()