import unittest

from prepare_classifyunits.classify_units import convert_classifyunits


class TestNLPTools(unittest.TestCase):
    @unittest.skip
    def test_split_text_into_paragraphs(self):
        example_input = "Wir stellen ab sofort ein:\n\nAltenpflegehelfer/in\n\nWas Sie mitbringen " \
                        "sollten:\n-Abgeschlossenes Studium\n-Gute Sprachkenntnisse in Deutsch und Englisch"

        example_output = ["Wir stellen ab sofort ein:", "Altenpflegehelfer/in", "Was Sie mitbringen "
                                                                                "sollten:\n-Abgeschlossenes "
                                                                                "Studium\n-Gute Sprachkenntnisse in "
                                                                                "Deutsch und Englisch"]

        # TODO Methode bekommt als Parameter ein Objekt der Klasse JobAds und keinen String übergeben
        self.assertEqual(convert_classifyunits.split_at_empty_line(example_input), example_output)

    # def test_remove_whitespaces(self):

    def test_identify_and_merge_listitems(self):
        example_input = ["Ihre Aufgabe:"
                         "* Identifizieren von Marktanforderungen und Kundenprojekten"
                         "* Technische Beratung und Betreuung von Kundenprojekten von der Planung bis zur Realisierung gemeinsam mit dem Vertriebsinnendienst"
                         "* Betreuung der Gebäudetechnik Planer"
                         "* Wettbewerbsbeobachtungen und -analysen",
                         "* Organisation und Durchführung von Fachvorträgen und Produktpräsentationen"
                         "* Teilnahme an Ausstellungen und Messen"
                         "* Einsatzgebiet Region Nord-/Ostdeutschland"
                         "* Homeoffice idealerweise in Berlin/Potsdam"]

        example_output = ["Ihre Aufgabe:\n"
                          "* Identifizieren von Marktanforderungen und Kundenprojekten\n"
                          "* Technische Beratung und Betreuung von Kundenprojekten von der Planung bis zur Realisierung gemeinsam mit dem Vertriebsinnendienst"
                          "* Betreuung der Gebäudetechnik Planer\n"
                          "* Wettbewerbsbeobachtungen und -analysen\n"
                          "* Organisation und Durchführung von Fachvorträgen und Produktpräsentationen\n"
                          "* Teilnahme an Ausstellungen und Messen\n"
                          "* Einsatzgebiet Region Nord-/Ostdeutschland\n"
                          "* Homeoffice idealerweise in Berlin/Potsdam"]

        self.assertEqual(convert_classifyunits.identify_listitems(example_input), example_output)
