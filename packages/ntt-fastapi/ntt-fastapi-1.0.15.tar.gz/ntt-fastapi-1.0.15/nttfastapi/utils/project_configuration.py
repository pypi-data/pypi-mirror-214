import os
from .file_system import *
from .ntt_argparser import *
from .command_line import *
from .virtual_env import *
from ..constants import *

class ProjectConfiguration:
    @classmethod
    def setup(self):
        folders = [
            APP_FOLDER,
            APP_API_FOLDER,
            APP_API_V1_FOLDER,
            APP_CONTROLLER_FOLDER,
            APP_SCHEMA_FOLDER,
            APP_UTIL_FOLDER,
            TEST_FOLDER,
            CONSTANTS_FOLDER,
            DATABASE_FOLDER,
            DATABASE_MODEL_FOLDER,
        ]

        project_name = NTTArgparser.parser.get_project_name()

        files = [
            (DOT_ENV_FILE_PATH, project_name),
            (DOT_EXAMPLE_ENV_FILE_PATH, project_name),
            (REQUIREMENT_FILE_PATH, project_name),
            (MAIN_FILE_PATH, project_name),
            (TEST_FILE_PATH, project_name),
            (TEST_ALL_FILE_PATH, project_name),
            (TEST_UNITTEST_FILE_PATH, project_name),
            (SERVER_FILE_PATH, project_name),
            (CONSTANT_ENV_FILE_PATH, os.path.join(project_name, CONSTANTS_FOLDER)),
            (DATABASE_BASE_FILE_PATH, os.path.join(project_name, DATABASE_FOLDER)),
        ]

        for folder in folders:
            full_folder_path = os.path.join(project_name, folder)
            NTTFileSystem.create_folder(folder_name=full_folder_path)
            NTTFileSystem.clone_file(src_path=INIT_FILE_PATH, des_path=full_folder_path)

        for src, des in files:
            NTTFileSystem.clone_file(src_path=src, des_path=des)

        VirtualEnv.install_package(requirement=os.path.join(project_name, REQUIREMENT_FILE))