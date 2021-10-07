"""Script to extract entities from ExtractionUnit. Remove known entities and select extraction with specific
confidence. """

# ## Imports
import logger
from information_extraction.extraction.ie_jobs import extract, remove_known_entities, evaluate_pattern, evaluate_seeds, \
    select_best_extractions
from orm_handling.models import ExtractionUnits, InformationEntity


# ## Function
def extract_entities(extraction_unit: ExtractionUnits, ie_mode: str) -> 'list[InformationEntity]':
    """Function to navigate through each step of extraction.
            * Step 1: Extract entities from given ExtractionUnit.
            * Step 2: Remove known entities to get only new ones.
            * Step 3: Evaluate used pattern for extraction and found extraction to compute confidence
                and select best ones.

            Parameters:
            ----------
                extraction_unit: ExtractionUnits
                    Receives an object from class ExtractionUnits.
                ie_mode: str
                    Receives an string with selected ie_mode.

            Returns:
            -------
                list with extracted entities from class InformationEntity"""

    # Step 1: extraction
    extractions = extract(extraction_unit, ie_mode)

    logger.log_ie.info(f'{len(extractions)} extracted entities from {ie_mode} were found in EU: {extraction_unit.id}.')

    # Step 2: remove extraction that that are already known
    extractions = remove_known_entities(extractions, ie_mode)

    # Step 3: evaluation of pattern and extraction and select best ones
    evaluate_pattern(extractions)
    evaluate_seeds(extractions)
    extractions = select_best_extractions(extractions)

    logger.log_ie.info(f'After removing known extractions and poorly rated ones, {len(extractions)} '
                       f' extractions from {ie_mode} remain.')

    return extractions
