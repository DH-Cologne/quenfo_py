from orm_handling.models import ClassifyUnits
from . import extraction_units


def generate_extractionunits(classifyunit: ClassifyUnits, ie_mode: str):
    extraction_units.get_extractionunits(classifyunit, ie_mode)

