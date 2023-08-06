import unittest
from unittest.mock import *

from nttfastapi.utils import *
from nttfastapi.constants import *
from tests.constants import *


class TestFileSystem(unittest.TestCase):
    @patch('os.makedirs')
    @patch('os.path.exists', side_effect=lambda x: False)
    def test_file_system_create_folder(self, make_dirs, path_exists):
        NTTFileSystem.create_folder(folder_name=TEST_PROJECT_NAME)

        make_dirs.assert_called_once_with(TEST_PROJECT_NAME)

    @patch('shutil.copy2')
    def test_clone_file(self, clone_file):
        NTTFileSystem.clone_file(
            src_path=TEST_SRC_PATH,
            des_path=TEST_DES_PATH,
        )

        clone_file.assert_called_once_with(
            TEST_SRC_PATH,
            TEST_DES_PATH,
        )