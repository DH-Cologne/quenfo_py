from orm_handling.models import ClassifyUnits
from . import extraction_units


def generate_extractionunits(classifyunit: ClassifyUnits):
    extractionunits = extraction_units.get_extractionunits(classifyunit)

