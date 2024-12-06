import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.colorlite.main import Logger



class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    @patch('sys.stdout', new_callable=StringIO)
    def test_debug(self, mock_stdout):
        self.logger.debug("This is a debug message.")
        self.assertEqual(mock_stdout.getvalue(),
                         "\033[94m\033[1mDEBUG:\033[0m This is a debug message.\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, mock_stdout):
        self.logger.info("This is an info message.")
        self.assertEqual(mock_stdout.getvalue(),
                         "\033[92m\033[1mINFO:\033[0m This is an info message.\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning(self, mock_stdout):
        self.logger.warning("This is a warning message.")
        self.assertEqual(mock_stdout.getvalue(),
                         "\033[93m\033[1mWARNING:\033[0m This is a warning message.\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_error(self, mock_stdout):
        self.logger.error("This is an error message.")
        self.assertEqual(mock_stdout.getvalue(),
                         "\033[91m\033[1mERROR:\033[0m This is an error message.\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_critical(self, mock_stdout):
        self.logger.critical("This is a critical message.")
        self.assertEqual(mock_stdout.getvalue(),
                         "\033[95m\033[1mCRITICAL:\033[0m This is a critical message.\n")

    # This test is calling all the methods to check if they are working as expected
    def test_example_usage(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            logger = Logger()
            logger.debug("This is a debug message.")
            logger.info("This is an info message.")
            logger.warning("This is a warning message.")
            logger.error("This is an error message.")
            logger.critical("This is a critical message.")
            self.assertEqual(mock_stdout.getvalue(),
                             "\033[94m\033[1mDEBUG:\033[0m This is a debug message.\n"
                             "\033[92m\033[1mINFO:\033[0m This is an info message.\n"
                             "\033[93m\033[1mWARNING:\033[0m This is a warning message.\n"
                             "\033[91m\033[1mERROR:\033[0m This is an error message.\n"
                             "\033[95m\033[1mCRITICAL:\033[0m This is a critical message.\n")

if __name__ == '__main__':
    unittest.main()


