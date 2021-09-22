import sys

import classification
import configuration
import database
import logger
from database import session
from information_extraction.prepare_extractionunits import generate_extractionunits
from orm_handling import orm


def extract():
    """Step 1: Set Connection to DB and load ClassifyUnits from DB. •
    Step 2: Check if table extraction_units and extractions exist, if not create new table. •
    Step 3: Check config: mode (overwrite or append), query limit etc. -> get_classify_units()
    Step 4: Load resources (lists, pattern) -> prepare_resources/init.py •
    Step 5: generate_extractionunits() from ClassifyUnits with class id 2 and 3 (use parameter: tool or competences)
    and write them in DB. •
    Step 6: Extract entities from extraction_units.
    Step 7: Remove known entities.
    Step 8: Evaluation of entities: conf.
    Step 9: Write extractions in DB."""

    # ## Set Variables
    query_limit = configuration.config_obj.get_ie_query_limit()  # query_limit: Number of ClassifyUnits to process
    if query_limit == -1:  # if query_limit is -1, the whole table will be processed.
        query_limit = orm.get_length('cu')  # Therefore the length of the table is extracted and set as query_limit.

    start_pos = configuration.config_obj.get_ie_start_pos()  # start_pos: Row Number where to start query
    current_pos = start_pos  # set row number for query
    counter = 0  # set counter in fetch_size steps
    cu_counter = 1  # set cu counter for each cu

    logger.log_ie.info(f'\n\nInformation Extraction starts.')
    print(f'Information Extraction starts.')
    logger.log_ie.info(f'The query_limit is set to {query_limit}.\
               The start_pos is {start_pos}.')

    # process cus as long as the conditions are met
    while True:
        # Step 1: Load the Input data: ClassifyUnits in ClassifyUnits Class.
        classify_units = orm.get_classify_units(current_pos)

        # Break if no more ClassifyUnits are found or query_limit is reached/exceeded.
        if len(classify_units) == 0:
            logger.log_ie.info(f'No more ClassifyUnits in batch. Stop processing.')
            break
        if counter >= query_limit:
            logger.log_ie.info(f'Query_limit reached. Stop processing.')
            break

        logger.log_ie.info(
            f'New chunk of ClassifyUnits loaded. Start processing --> generate_extractionunits.')

        # iterate over each cu
        for cu in classify_units:
            generate_extractionunits(cu)
            # add obj to current session --> to be written in db
            orm.create_output(database.session, cu)
            # Update progress in progress bar
            __progress(cu_counter, query_limit,
                       status=f" of {query_limit} ClassifyUnits generated. Current ClassifyUnit {cu_counter}.")
            cu_counter += 1

        # Commit generated extraction units to table
        orm.pass_output(database.session)
        counter += len(classify_units)  # update counter
        current_pos += len(classify_units)  # update current position

        logger.log_ie.info(
            f'session is cleaned and every obj of current batch is flushed: {database.session._is_clean()}.\
                Continue with next batch from current row position: {current_pos}.')

        orm.close_session(database.session)  # Close session
        print()
        logger.log_ie.info(f'InformationExtraction done. Return to main-level.')


# TODO Methode wird auch bei Classification genutzt
# Progress Bar to keep track of already processed ClassifyUnits
def __progress(count: int, total: int, status: str):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
