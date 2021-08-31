from database import session
from information_extraction.models import Configuration
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

    # Step 1: Load the Input data: ClassifyUnits in ClassifyUnits Class.
    classify_units = orm.get_classify_units()

    for cu in classify_units:
        generate_extractionunits(cu)
        orm.create_output(session, cu)

    # Commit generated classify units with paragraphs and classes to table
    orm.pass_output(session)
    # Close session
    orm.close_session(session)

