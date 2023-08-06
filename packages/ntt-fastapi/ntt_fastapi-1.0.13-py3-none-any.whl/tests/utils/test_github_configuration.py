# ------------ path configuration ------------- 
import sys
sys.path.append('nttfastapi')
sys.path.append('nttfastapi/utils')
# ------------ path configuration ------------- 

# ------------ python package ------------- 
import unittest
from unittest.mock import *
# ------------ python package ------------- 

# ------------ project package ------------
from nttfastapi.constants import *
from nttfastapi.utils import *
from tests.constants import *
from tests.tools import *
# ------------ project package ------------


class TestGithubConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        NTTArgparser()

    def test_configuration_with_copying_the_dot_gitignore_file(self):
        copy_file_func = MagicMock()
        NTTFileSystem.clone_file = copy_file_func
        
        run_command_func = MagicMock()
        NTTCommandLine.run_command = run_command_func

        mock_project_name(DEFAULT_PROJECT_FOLDER)

        GithubConfiguration.setup()

        project_name = NTTArgparser.parser.get_project_name()
        dot_git_ignore_path = os.path.join(project_name, GIT_IGNORE_FILE)

        copy_file_func.assert_called_with(
            src_path=GIT_IGNORE_PATH,
            des_path=dot_git_ignore_path
        )

        expected_calls = [
            call(command=INIT_GIT_COMMAND, folder_path=project_name),
            call(command=ADD_ALL_TO_GIT_COMMAND, folder_path=project_name),
            call(command=FIRST_COMMIT_COMMAND, folder_path=project_name),
            # call(command=CREATE_BRANCH_COMMAND, folder_path=project_name),
        ]

        run_command_func.assert_has_calls(expected_calls)