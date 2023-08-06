import unittest
from unittest.mock import *

from nttfastapi.utils import *
from nttfastapi.constants import *

from tests.constants import *


class TestCommandLine(unittest.TestCase):
    @patch('subprocess.run')
    def test_run_command(self, run_command):
        command = 'py --version'
        NTTCommandLine.run_command(
            command=command,
        )

        run_command.assert_called_once_with(
            args=command.split(' '),
        )

    @patch('subprocess.run')
    def test_run_command_with_folder_path(self, run_command):
        command = 'py --version'
        NTTCommandLine.run_command(
            command=command,
            folder_path=TEST_FOLDER_PATH,
        )

        run_command.assert_called_once_with(
            args=command.split(' '),
            cwd=TEST_FOLDER_PATH,
        )