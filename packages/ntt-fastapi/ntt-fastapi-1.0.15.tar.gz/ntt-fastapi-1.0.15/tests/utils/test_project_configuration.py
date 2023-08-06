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


class TestProjectConfiguration(unittest.TestCase):
    def test_config_project(self):
        create_folder_func = MagicMock()
        clone_file_func = MagicMock()
        install_func = MagicMock()
        NTTFileSystem.create_folder = create_folder_func
        NTTFileSystem.clone_file = clone_file_func
        # VirtualEnv.install_package = install_func
        

        mock_project_name(TEST_FOLDER_PATH)

        ProjectConfiguration.setup()


        expected_calls = [
            call(folder_name=os.path.join(TEST_FOLDER_PATH, APP_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, APP_API_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, APP_API_V1_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, APP_CONTROLLER_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, APP_SCHEMA_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, APP_UTIL_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, TEST_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, CONSTANTS_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, DATABASE_FOLDER)),
            call(folder_name=os.path.join(TEST_FOLDER_PATH, DATABASE_MODEL_FOLDER)),
        ]


        clone_expected_calls = [
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, APP_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, APP_API_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, APP_API_V1_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, APP_CONTROLLER_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, APP_SCHEMA_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, APP_UTIL_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, TEST_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, CONSTANTS_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, DATABASE_FOLDER)),
            call(src_path=INIT_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, DATABASE_MODEL_FOLDER)),
            call(src_path=DOT_ENV_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=DOT_EXAMPLE_ENV_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=REQUIREMENT_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=MAIN_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=TEST_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=TEST_ALL_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=TEST_UNITTEST_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=SERVER_FILE_PATH, des_path=TEST_FOLDER_PATH),
            call(src_path=CONSTANT_ENV_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, CONSTANTS_FOLDER)),
            call(src_path=DATABASE_BASE_FILE_PATH, des_path=os.path.join(TEST_FOLDER_PATH, DATABASE_FOLDER)),
        ]

        create_folder_func.assert_has_calls(expected_calls)
        clone_file_func.assert_has_calls(clone_expected_calls)
        install_func.assert_called_with(
            requirement=os.path.join(TEST_FOLDER_PATH, REQUIREMENT_FILE)
        )