import unittest
import logger

class TestLogging(unittest.TestCase):
    # Set all logger
    logger.main()

    def test_log_main(self):
        # Test log_main
        with self.assertLogs('log_main', level='INFO') as captured:
            logger.log_main.info("Test Logger Main.")
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), "Test Logger Main.")

    def test_log_clf(self):
        # Test log_clf
        with self.assertLogs('log_clf', level='INFO') as captured:
            logger.log_clf.info("Test Logger Clf.")
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), "Test Logger Clf.")

    def test_log_ie(self):
        # Test log_ie
        with self.assertLogs('log_ie', level='INFO') as captured:
            logger.log_ie.info("Test Logger ie.")
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), "Test Logger ie.")

    def test_log_match(self):
        # Test log_match
        with self.assertLogs('log_match', level='INFO') as captured:
            logger.log_match.info("Test Logger match.")
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), "Test Logger match.")


if __name__ == '__main__':
    unittest.main()