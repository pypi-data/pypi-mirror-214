# # ------------ path configuration ------------- 
# import sys
# sys.path.append('nttfastapi')
# sys.path.append('nttfastapi/utils')
# # ------------ path configuration ------------- 

# ------------ python package ------------- 
import unittest
from unittest.mock import *
# ------------ python package ------------- 

# ------------ project package ------------
from nttfastapi.constants import *
from nttfastapi.utils import *
from nttfastapi.cli import *
# ------------ project package ------------


class TestCreateProjectFolder(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_default_project_with_given_project_name(self):
        create_folder_func = MagicMock()
        NTTFileSystem.create_folder = create_folder_func

        setup_venv_func = MagicMock()
        VirtualEnv.setup = setup_venv_func

        setup_github_func = MagicMock()
        GithubConfiguration.setup = setup_github_func

        config_project = MagicMock()
        ProjectConfiguration.setup = config_project

        create_folder_action(DEFAULT_PROJECT_FOLDER)

        create_folder_func.assert_called_with(
            folder_name=DEFAULT_PROJECT_FOLDER
        )

        setup_venv_func.assert_called_with(
            folder_name=DEFAULT_VENV_FOLDER
        )

        setup_github_func.assert_called_once()

        config_project.assert_called_once()