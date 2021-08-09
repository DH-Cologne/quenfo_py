import unittest
from pathlib import Path

import yaml

from prepare_classifyunits.classify_units import convert_classifyunits
from prepare_classifyunits.feature_units import convert_featureunits

with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    fus_config = cfg['fus_config']
    resources = cfg['resources']


class TestNLPTools(unittest.TestCase):
    def test_split_text_into_paragraphs(self):
        example_input = "Wir stellen ab sofort ein:\n\nAltenpflegehelfer/in\n\nWas Sie mitbringen " \
                        "sollten:\n-Abgeschlossenes Studium\n-Gute Sprachkenntnisse in Deutsch und Englisch"

        example_output = ["Wir stellen ab sofort ein:", "Altenpflegehelfer/in", "Was Sie mitbringen "
                                                                                "sollten:\n-Abgeschlossenes "
                                                                                "Studium\n-Gute Sprachkenntnisse in "
                                                                                "Deutsch und Englisch"]

        self.assertEqual(convert_classifyunits.split_at_empty_line(example_input), example_output)

    def test_remove_whitespaces(self):
        test_input = ["     Wir stellen ab sofort ein:\n\nAltenpflegehelfer/in\n\nWas Sie mitbringen "
                      "sollten:\n-Abgeschlossenes Studium\n-Gute Sprachkenntnisse in Deutsch und Englisch           ",
                      "             Technischer Zeichner für Tga Tech.Gebäudeausrüstung Technische / -r "
                      "Systemplaner / - in - Versorgungs - und "
                      "Ausrüstungst. GeHatec-Gesellschaft für Haustechnik Berlin mbH\n\n            ",
                      "             Ausbildungsplatz für 2018 als Technischer Zeichner für Tga Tech.Gebäudeausrüstung "
                      "Technische / -r Haustechnik Berlin mbH. \n"
                      "Aussagekräftige Bewerbung bitte direkt über den Bewerben - Button versenden.             "]

        test_output = ['Wir stellen ab sofort ein:\n\nAltenpflegehelfer/in\n\nWas Sie mitbringen '
                       'sollten:\n-Abgeschlossenes Studium\n-Gute Sprachkenntnisse in Deutsch und Englisch',
                       'Technischer Zeichner für Tga Tech.Gebäudeausrüstung Technische / -r Systemplaner / - in - '
                       'Versorgungs - und Ausrüstungst. GeHatec-Gesellschaft für Haustechnik Berlin mbH',
                       'Ausbildungsplatz für 2018 als Technischer Zeichner für Tga Tech.Gebäudeausrüstung Technische '
                       '/ -r Haustechnik Berlin mbH.\nAussagekräftige Bewerbung bitte direkt über den Bewerben - '
                       'Button versenden.']

        self.assertEqual(convert_classifyunits.remove_whitespaces(test_input), test_output)

    def test_identify_and_merge_listitems(self):
        example_input = ["Ihre Aufgabe:\n"
                         "* Identifizieren von Marktanforderungen und Kundenprojekten\n"
                         "* Technische Beratung und Betreuung von Kundenprojekten von der Planung bis zur "
                         "Realisierung gemeinsam mit dem Vertriebsinnendienst\n"
                         "* Betreuung der Gebäudetechnik Planer\n"
                         "* Wettbewerbsbeobachtungen und -analysen\n",
                         "* Organisation und Durchführung von Fachvorträgen und Produktpräsentationen\n"
                         "* Teilnahme an Ausstellungen und Messen\n"
                         "* Einsatzgebiet Region Nord-/Ostdeutschland\n"
                         "* Homeoffice idealerweise in Berlin/Potsdam"]

        example_output = ["Ihre Aufgabe:\n* Identifizieren von Marktanforderungen und Kundenprojekten\n* Technische "
                          "Beratung und Betreuung von Kundenprojekten von der Planung bis zur Realisierung gemeinsam "
                          "mit dem Vertriebsinnendienst\n* Betreuung der Gebäudetechnik Planer\n* "
                          "Wettbewerbsbeobachtungen und -analysen\n\n* Organisation und Durchführung von "
                          "Fachvorträgen und Produktpräsentationen\n* Teilnahme an Ausstellungen und Messen\n* "
                          "Einsatzgebiet Region Nord-/Ostdeutschland\n* Homeoffice idealerweise in Berlin/Potsdam"]

        self.assertEqual(convert_classifyunits.identify_listitems(example_input), example_output)
        self.assertIsInstance(convert_classifyunits.identify_listitems(example_input), list)

    def test_mergewhatbelongstogether(self):
        test_input = [
            "Technischer Zeichner für Tga Tech. Gebäudeausrüstung Technische/-r Systemplaner/-in - Versorgungs- und "
            "Ausrüstungst. GeHatec-Gesellschaft für Haustechnik Berlin mbH "
            "Ausbildungsplatz für 2018 als Technischer Zeichner für Tga Tech.Gebäudeausrüstung Technische / -r "
            "Systemplaner / - in - Versorgungs - und Ausrüstungst. in Berlin bei GeHatec - Gesellschaft für "
            "Haustechnik Berlin mbH. Aussagekräftige Bewerbung bitte direkt über den Bewerben - Button "
            "versenden.\n",
            "Ein solides Handwerk kommt nicht aus der Mode. Egal welche technischen Neuerungen auf den Markt "
            "kommen, in unserer Ausbildung als Technischer Zeichner für Tga Tech.Gebäudeausrüstung Technische "
            " / -r Systemplaner / - in - Versorgungs - und Ausrüstungst.werden Innovationen aufgenommen "
            "und mit altbewährten Methoden ergänzt.Mit der Ausbildung zur / zum Technischer Zeichner.\n",
            "  Anforderungsprofil\n"
            "+ Erfahrung in der Terminplanung\n"
            "+ Abgeschlossenes betriebswirtschaftliches Studium wünschenswert\n"
            "+ Pflege des Projektplans und des Kostenplans\n"
            "+ Freundliches Auftreteten, auch in schwierigen Situationen\n"
            "+ Sichere Deutsch- und Arabischkenntnisse in Wort und Schrift\n"
            "+ Kontakte zu arabischsprachigen Experte/-innen, Lotse/-innen und ehrenamtlichen Helfer/-innen\n"
            "+ Erfahrung mit MS Office"]

        test_output = ['Technischer Zeichner für Tga Tech. Gebäudeausrüstung Technische/-r Systemplaner/-in - '
                       'Versorgungs- und Ausrüstungst. GeHatec-Gesellschaft für Haustechnik Berlin mbH '
                       'Ausbildungsplatz für 2018 als Technischer Zeichner für Tga Tech.Gebäudeausrüstung Technische '
                       '/ -r Systemplaner / - in - Versorgungs - und Ausrüstungst. in Berlin bei GeHatec - '
                       'Gesellschaft für Haustechnik Berlin mbH. Aussagekräftige Bewerbung bitte direkt über den '
                       'Bewerben - Button versenden.\n\nEin solides Handwerk kommt nicht aus der Mode. Egal welche '
                       'technischen Neuerungen auf den Markt kommen, in unserer Ausbildung als Technischer Zeichner '
                       'für Tga Tech.Gebäudeausrüstung Technische  / -r Systemplaner / - in - Versorgungs - und '
                       'Ausrüstungst.werden Innovationen aufgenommen und mit altbewährten Methoden ergänzt.Mit der '
                       'Ausbildung zur / zum Technischer Zeichner.\n', '  Anforderungsprofil\n+ Erfahrung in der '
                                                                       'Terminplanung\n+ Abgeschlossenes '
                                                                       'betriebswirtschaftliches Studium '
                                                                       'wünschenswert\n+ Pflege des Projektplans und '
                                                                       'des Kostenplans\n+ Freundliches Auftreteten, '
                                                                       'auch in schwierigen Situationen\n+ Sichere '
                                                                       'Deutsch- und Arabischkenntnisse in Wort und '
                                                                       'Schrift\n+ Kontakte zu arabischsprachigen '
                                                                       'Experte/-innen, Lotse/-innen und '
                                                                       'ehrenamtlichen Helfer/-innen\n+ Erfahrung mit '
                                                                       'MS Office']

        self.assertEqual(convert_classifyunits.identify_whatbelongstogether(test_input), test_output)
        self.assertIsInstance(convert_classifyunits.identify_whatbelongstogether(test_input), list)

    def test_replace_non_alphanumerical(self):
        test_input = "Für ein Gesundheitsinstitut in Berlin-Pankow suchen wir aktuell eine/n " \
                     "Personalsachbearbeiter/in (mit Lohnkenntnissen) oder eine/n Personalreferent/in in Voll- oder " \
                     "Teilzeit. Sie werden angemessen mit einem Gehalt von 2880,-?/Monat vergütet. "

        test_output = "Für ein Gesundheitsinstitut in Berlin Pankow suchen wir aktuell eine n Personalsachbearbeiter " \
                      "in mit Lohnkenntnissen oder eine n Personalreferent in in Voll oder Teilzeit Sie werden " \
                      "angemessen mit einem Gehalt von 2880 Monat vergütet "

        self.assertEqual(convert_featureunits.replace(test_input), test_output)
        self.assertIsInstance(convert_featureunits.replace(test_input), str)

    def test_tokenize(self):
        test_input = "Wir suchen Personal."

        test_output = ["Wir", "suchen", "Personal"]

        self.assertEqual(convert_featureunits.tokenize(test_input), test_output)
        self.assertIsInstance(convert_featureunits.tokenize(test_input), list)

    def test_normalize(self):
        test_input = ["Wir", "suchen", "Personal", "1234"]

        test_output = ["wir", "suchen", "personal", "NUM"]

        self.assertEqual(convert_featureunits.normalize(test_input, True), test_output)
        self.assertIsInstance(convert_featureunits.normalize(test_input, True), list)

    def test_filterSW(self):
        test_input = ['beschreibung', 'es', 'werden', 'NUM', 'pflegehelfer', 'mit', 'vermittlungsgutschein', 'gesucht',
                      'ihre', 'aufgaben', 'die', 'grundlegende', 'hygiene', 'von', 'patienten', 'und', 'bewohnern',
                      'hilfe', 'beim', 'waschen', 'und', 'ankleiden', 'sie', 'unterstützen', 'in', 'der',
                      'essensversorgung', 'und', 'helfen', 'ihre', 'kollegen', 'sie', 'betreuen', 'patienten', 'im',
                      'alltag', 'die', 'dokumentation', 'rundet', 'ihren', 'ereignisreichen', 'tag', 'ab']

        test_output = ['beschreibung', 'es', 'werden', 'NUM', 'pflegehelfer', 'vermittlungsgutschein', 'gesucht',
                       'ihre', 'aufgaben', 'grundlegende', 'hygiene', 'patienten', 'bewohnern', 'hilfe', 'waschen',
                       'ankleiden', 'sie', 'unterstützen', 'essensversorgung', 'helfen', 'ihre', 'kollegen', 'sie',
                       'betreuen', 'patienten', 'alltag', 'dokumentation', 'rundet', 'ihren', 'ereignisreichen', 'tag']

        self.assertEqual(convert_featureunits.filterSW(test_input, True, Path(resources['stopwords_path'])),
                         test_output)
        self.assertIsInstance(convert_featureunits.filterSW(test_input, True, Path(resources['stopwords_path'])), list)

    def test_stemming(self):
        test_input = ['beschreibung', 'es', 'werden', 'NUM', 'pflegehelfer', 'vermittlungsgutschein', 'gesucht', 'ihre',
                      'aufgaben', 'grundlegende', 'hygiene', 'patienten', 'bewohnern', 'hilfe', 'waschen', 'ankleiden',
                      'sie', 'unterstützen', 'essensversorgung', 'helfen', 'ihre', 'kollegen', 'sie', 'betreuen',
                      'patienten', 'alltag', 'dokumentation', 'rundet', 'ihren', 'ereignisreichen', 'tag']

        test_output = ['beschreib', 'es', 'werd', 'num', 'pflegehelf', 'vermittlungsgutschein', 'gesucht', 'ihr',
                       'aufgab', 'grundleg', 'hygi', 'patient', 'bewohn', 'hilf', 'wasch', 'ankleid', 'sie',
                       'unterstutz', 'essensversorg', 'helf', 'ihr', 'kolleg', 'sie', 'betreu', 'patient', 'alltag',
                       'dokumentation', 'rundet', 'ihr', 'ereignisreich', 'tag']

        self.assertEqual(convert_featureunits.stem(test_input, True), test_output)
        self.assertIsInstance(convert_featureunits.stem(test_input, True), list)

    def test_generate_ngrams(self):
        test_input = ["Wir", "suchen", "Personal"]

        test_output = ["Wir", "suc", "uch", "che", "hen",
                       "Per", "ers", "rso", "son", "ona",
                       "nal",
                       "such", "uche", "chen", "Pers",
                       "erso", "rson", "sona", "onal"]

        self.assertEqual(
            convert_featureunits.gen_ngrams(test_input, fus_config["nGrams"], fus_config["continuousNGrams"]),
            test_output)
        self.assertIsInstance(
            convert_featureunits.gen_ngrams(test_input, fus_config["nGrams"], fus_config["continuousNGrams"]), list)
