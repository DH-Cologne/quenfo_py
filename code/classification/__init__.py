""" Script to handle the classification.
    * Step 1: Load JobAds
    * Step 2: Generate CUs (and also fus and fvs) from JobAds
    * Step 3: Predict Classes for CUs """

# ## Imports
from . import prepare_classifyunits
from . import predict_classes
import database
from orm_handling import orm
from training.train_models import Model
import configuration
import sys
import logger

# ## Function
def classify(model: Model) -> None:
    """ Classify JobAds
    * Step 1: Load JobAds
    * Step 2: Generate CUs (and also fus and fvs) from JobAds
    * Step 3: Predict Classes for CUs 

    Parameters
    ----------
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information """

    # ## Set Variables
    query_limit = configuration.config_obj.get_query_limit()    # query_limit: Number of JobAds to process
    if query_limit == -1:                                       # if query_limit is -1, the whole table will be processed.
        query_limit = orm.get_length()                          # Therefore the length of the table is extracted and set as query_limit.

    start_pos = configuration.config_obj.get_start_pos()        # start_pos: Row Number where to start query
    current_pos = start_pos                                     # set row number for query
    counter = 0                                                 # set counter in fetch_size steps
    jobad_counter = 1                                           # set jobad counter for each jobad

    logger.log_clf.info(f'\n\nClassification of JobAds starts.')
    print(f'Classification of JobAds starts.')
    logger.log_clf.info(f'The query_limit is set to {query_limit}.\
            The start_pos is {start_pos}.')

    # process jobads as long as the conditions are met
    while True:
        # STEP 1: Load the Input data: JobAds in JobAds Class.
        jobads = orm.get_jobads(current_pos)
    
        # Break if no more JobAds are found or query_limit is reached/exceeded.
        if len(jobads) == 0:
            logger.log_clf.info(f'No more JobAds in batch. Stop processing.')
            break
        if counter >= query_limit:
            logger.log_clf.info(f'Query_limit reached. Stop processing.')
            break

        logger.log_clf.info(f'New chunk of jobads loaded. Start processing --> generate_classifyunits and start_prediction.')
        # iterate over each jobad
        for jobad in jobads:
            # STEP 2: Generate classify_units, feature_units and feature_vectors for each JobAd.
            prepare_classifyunits.generate_classifyunits(jobad, model)
            # STEP 3: Predict Classes for CUs in JobAds. 
            predict_classes.start_prediction(jobad, model)
            # add obj (with predicted paragraphs) to current session --> to be written in db
            orm.create_output(database.session, jobad)
            # Update progress in progress bar
            __progress(jobad_counter, query_limit, status=f" of {query_limit} JobAds classified. Current JobAd {jobad_counter}.")
            jobad_counter += 1

        # Commit generated classify units with paragraphs and classes to table
        orm.pass_output(database.session)
        counter += len(jobads)              # update counter
        current_pos += len(jobads)          # update current position

        logger.log_clf.info(f'session is cleaned and every obj of current batch is flushed: {database.session._is_clean()}.\
            Continue with next batch from current row position: {current_pos}.')
    
    orm.handle_td_changes(model)            # Reset traindata changes (used as filler)
    orm.close_session(database.session)     # Close session
    print()
    logger.log_clf.info(f'Classification done. Return to main-level.')

# Progress Bar to keep track of already processed JobAds
def __progress(count: int, total: int, status: str):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()