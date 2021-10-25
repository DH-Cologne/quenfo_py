""" Script to handle the information extraction.
    * Step 1: Load ClassifyUnits
    * Step 2: Generate EUs from CUs
    * Step 3: Extract Entities"""

# ## Imports
import sys
import configuration
import database
import logger
from information_extraction.extraction import extract_entities
from information_extraction.prepare_extractionunits import generate_extraction_units
from orm_handling import orm


# ## Functions
from orm_handling.models import ClassifyUnits


def extract():
    """Main-Function for Information Extraction.
        * Step 1: Set Connection to DB and load ClassifyUnits from DB -> get_classify_units
        * Step 2: For each CU generate ExtractionUnits (sentences) -> generate_extractionunits
        * Step 3: Load EUs from DB -> get_extraction_units
        * Step 4: For each EU extract entities -> extract_entities"""

    # ## Set Variables
    all_extractions = list()  # list with all found extractions

    query_limit = configuration.config_obj.get_ie_query_limit()  # query_limit: Number of ClassifyUnits to process
    search_type = configuration.config_obj.get_search_type()
    if query_limit == -1:  # if query_limit is -1, the whole table will be processed.
        cus = database.session.query(ClassifyUnits).order_by('id').filter(
        ClassifyUnits.classID == search_type).all()
        query_limit = len(cus)  # Therefore the length of the table is extracted and set as query_limit.

    start_pos = configuration.config_obj.get_ie_start_pos()  # start_pos: Row Number where to start query
    current_pos = start_pos  # set row number for query
    counter = 0  # set counter in fetch_size steps
    cu_counter = 1  # set cu counter for each cu
    eu_counter = 1  # set eu counter for each eu

    ie_mode = set_ie_mode(configuration.config_obj.get_ie_type())

    logger.log_ie.info(f'\n\nInformation Extraction starts.')
    logger.log_ie.info(f'The query_limit is set to {query_limit}.\
               The start_pos is {start_pos}.')
    print(f'\n\nGeneration of ExtractionUnits starts.')
    logger.log_ie.info(f'Generation of ExtractionUnits starts.')

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
            # Step 2: Generate EUs -> sentences
            generate_extraction_units(cu, ie_mode)
            # add obj to current session --> to be written in db
            orm.create_output(database.session, cu, 'eu')
            # Update progress in progress bar
            __progress(cu_counter, query_limit,
                       status=f" of {query_limit} ClassifyUnits separated. "
                              f"Current ClassifyUnit {cu_counter}.")
            cu_counter += 1

        # Commit generated extraction units to table
        orm.pass_output(database.session)
        counter += len(classify_units)  # update counter
        current_pos += len(classify_units)  # update current position

        logger.log_ie.info(
            f'session is cleaned and every obj of current batch is flushed: {database.session._is_clean()}.\
                Continue with next batch from current row position: {current_pos}.')

    print()

    # Step 3: Load EUs from DB
    extraction_units = orm.get_extraction_units()

    logger.log_ie.info(f'{len(extraction_units)} ExtractionUnits load from db.\n\nExtraction starts.')
    print(f'{len(extraction_units)} ExtractionUnits load from db.\n\nExtraction starts.')

    # iterate over each eu
    for eu in extraction_units:
        # Step 4: Extraction
        extractions = extract_entities(eu, ie_mode)
        all_extractions.extend(extractions)  # collect all extractions
        # add obj to current session --> to be written in db
        orm.create_output(database.session, eu, 'e')
        # Update progress in progress bar
        __progress(eu_counter, len(extraction_units), status=f" of {len(extraction_units)} ExtractionUnits processed. "
                                                             f"Current ExtractionUnit {eu_counter}.")
        eu_counter += 1

    # Commit generated extractions to table
    orm.pass_output(database.session)

    logger.log_ie.info(f'{len(all_extractions)} extracted entities from {ie_mode} were found.')
    orm.close_session(database.session)  # Close session
    print()
    logger.log_ie.info(f'InformationExtraction done. Return to main-level.')


def set_ie_mode(ie_types: dict) -> str:
    """Function to set ie_mode: COMPETENCES, TOOLS or COMPETENCES AND TOOLS

            Parameters:
            ----------
                ie_types: dict
                    Receives a dict from config.yaml

            Returns:
            -------
                str with ie_mode"""

    if ('tools', True) in ie_types.items():
        ie_mode = "TOOLS"
    elif ('competences', True) in ie_types.items():
        ie_mode = "COMPETENCES"
    elif ('tools', True) in ie_types.items() and ('competences', True) in ie_types.items():
        ie_mode = "COMPETENCES AND TOOLS"
    else:
        ie_mode = "TYPE OF EXTRACTION NOT GIVEN"
    return ie_mode


# Progress Bar to keep track of already processed objects from class
def __progress(count: int, total: int, status: str):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
