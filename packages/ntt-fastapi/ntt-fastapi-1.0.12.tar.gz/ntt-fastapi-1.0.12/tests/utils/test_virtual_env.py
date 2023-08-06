import unittest
from unittest.mock import *

from nttfastapi.utils import *
from nttfastapi.constants import *

from tests.constants import *
from tests.tools import *


class TestVirtualEnv(unittest.TestCase):
    def setUp(self) -> None:
        mock_project_name(TEST_FOLDER_PATH)

        self.run_command_func = MagicMock()
        NTTCommandLine.run_command = self.run_command_func

    def test_virtual_env_setup(self):
        VirtualEnv.setup(folder_name=DEFAULT_VENV_FOLDER)

        test_venv_folder = os.path.join(NTTArgparser.parser.get_project_name(), DEFAULT_VENV_FOLDER)

        expected_calls = [
            call(command=INSTALL_VIRTUALENV_COMMAND),
            call(command=f"{CREAT_VIRTUAL_ENV_COMMAND} {test_venv_folder}"),
        ]

        self.run_command_func.assert_has_calls(expected_calls)

    def test_install(self):
        VirtualEnv.install_package(package=TEST_PACKAGE)
        python_exe = os.path.join(TEST_FOLDER_PATH, DEAFULT_VENV_PYTHON_EXE)

        self.run_command_func.assert_called_once_with(
            command=f"{python_exe} -m pip install {TEST_PACKAGE}"
        )

    def test_install_by_requirement(self):
        VirtualEnv.install_package(requirement=TEST_REQUIREMENT)
        python_exe = os.path.join(TEST_FOLDER_PATH, DEAFULT_VENV_PYTHON_EXE)

        self.run_command_func.assert_called_once_with(
            command=f"{python_exe} -m pip install -r {TEST_REQUIREMENT}"
        )