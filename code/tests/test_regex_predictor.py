import unittest

class TestRegexPredictor(unittest.TestCase):
    def test_input(self):
        # hier kann man den type überprüfen, ist die instanz aus connection.session ein Session obj
        self.assertIsInstance(connection.session, Session, "Session to database is not ready.")
        # hier zb selber festlegen was der output sein soll und geben dann den input ein assert equal, schau ob die gleich sind
        self.assertEqual(convert_classifyunits.remove_whitespaces(test_input), test_output)

    def test_output(self):
        self.assertIsInstance(connection.engine, Engine, "Engine from session is not ready.")


if __name__ == '__main__':
    unittest.main()