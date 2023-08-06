# Copyright (C) 2023, NG:ITL
import logging
import tempfile
import unittest
import re
import abc

from pathlib import Path

from ngitl_common_py.log import init_logging, init_emergency_logging, get_log_filepath, flush


class LogTest(unittest.TestCase):

    TEST_COMPONENT_NAME = "unittest"

    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.init_log()

    @abc.abstractmethod
    def init_log(self):
        raise NotImplementedError

    # def find_log_file(self) -> Optional[Path]:
    #     elements = os.listdir(self.tmp_dir)
    #     for element in elements:
    #         if re.search(r"(\d{8}-\d{6}_|)unittest(_emergency|)\.log", element):
    #             return self.tmp_dir / element

    def log_test_lines(self):
        logging.debug("log line 1")
        logging.info("log line 2")
        logging.warning("log line 3")
        logging.error("log line 4")

    def assert_log_line(self, expected_line_as_regex: str):
        flush()
        with open(get_log_filepath(), "r") as log_file:
            lines = log_file.readlines()
            for line in lines:
                if re.search(expected_line_as_regex, line):
                    return
            self.fail(f"Unable to find expected line in log file: \"{expected_line_as_regex}\"")

    def assert_test_log_lines(self):
        self.assert_log_line(r"\[DEBUG\]\[test_log\]: log line 1$")
        self.assert_log_line(r"\[INFO\]\[test_log\]: log line 2$")
        self.assert_log_line(r"\[WARNING\]\[test_log\]: log line 3$")
        self.assert_log_line(r"\[ERROR\]\[test_log\]: log line 4$")

class RegularLogTest(LogTest):

    def init_log(self):
        init_logging(self.TEST_COMPONENT_NAME, self.tmp_dir, "DEBUG")

    def assert_regular_welcome_log_line(self):
        self.assert_log_line("Logging initialized!")

    def test_RegularLogInitialized_PrintLogLines_ExpectedLinesLogged(self) -> None:
        self.log_test_lines()
        self.assert_regular_welcome_log_line()
        self.assert_test_log_lines()


class EmergencyLogTest(LogTest):

    def init_log(self):
        init_emergency_logging(self.TEST_COMPONENT_NAME, log_file_directory=self.tmp_dir)

    def assert_emergency_welcome_log_line(self):
        self.assert_log_line("\[ERROR\]\[log\]: Emergency log initialized!$")

    def test_RegularLogInitialized_PrintLogLines_ExpectedLinesLogged(self) -> None:
        self.log_test_lines()
        self.assert_emergency_welcome_log_line()
        self.assert_test_log_lines()



