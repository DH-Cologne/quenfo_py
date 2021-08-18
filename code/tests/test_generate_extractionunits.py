import unittest

from information_extraction import connection_resources
from information_extraction.prepare_extractionunits.extraction_units import convert_extractionunits


class TestGenerateExtractionUnits(unittest.TestCase):
    def test_normalize_sentence(self):
        case1 = "Der Hund UND die Maus ,unerwartet ja, gehen nach Hause."
        case2 = "Sie mögen sich gerne ,ODER etwa nicht?"
        case3 = "Entweder sie haben sich gerne und/oder nicht."
        case4 = "Aber sie mögen beide Essen oder-UND kein Hungern."
        case5 = "Vielleicht sollten sie beide schlafen gehen UND oder nicht."
        case6 = "Ich mag Hausschuhe;aber keine Schuhe."
        case7 = "Kenntnisse in Java /Python"

        output1 = "Der Hund und die Maus , unerwartet ja, gehen nach Hause."
        output2 = "Sie mögen sich gerne , oder etwa nicht?"
        output3 = "Entweder sie haben sich gerne oder nicht."
        output4 = "Aber sie mögen beide Essen und kein Hungern."
        output5 = "Vielleicht sollten sie beide schlafen gehen oder nicht."
        output6 = "Ich mag Hausschuhe; aber keine Schuhe."
        output7 = "Kenntnisse in Java Python"

        self.assertEqual(convert_extractionunits.normalize_sentence(case1), output1)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case1), str)
        self.assertEqual(convert_extractionunits.normalize_sentence(case2), output2)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case2), str)
        self.assertEqual(convert_extractionunits.normalize_sentence(case3), output3)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case3), str)
        self.assertEqual(convert_extractionunits.normalize_sentence(case4), output4)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case4), str)
        self.assertEqual(convert_extractionunits.normalize_sentence(case5), output5)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case5), str)
        self.assertEqual(convert_extractionunits.normalize_sentence(case6), output6)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case6), str)
        self.assertEqual(convert_extractionunits.normalize_sentence(case7), output7)
        self.assertIsInstance(convert_extractionunits.normalize_sentence(case7), str)

    def test_get_entities_list(self):
        self.assertIsInstance(connection_resources.get_entities_from_file("tools"), list)
