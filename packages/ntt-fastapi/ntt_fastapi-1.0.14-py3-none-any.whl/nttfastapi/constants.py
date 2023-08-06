import os

# ========================= Default configuration
DEFAULT_PROJECT_FOLDER = 'ntt_fastapi_project'
CREATE_ACTION_NAME = "create"

DEFAULT_VENV_FOLDER = 'venv'
DEAFULT_VENV_PYTHON_EXE = os.path.join(DEFAULT_VENV_FOLDER, 'Scripts', 'python.exe')

INIT_GIT_COMMAND = "git init"
ADD_ALL_TO_GIT_COMMAND = "git add ."
FIRST_COMMIT_COMMAND = 'git commit -m \"First commit\"'
CREATE_BRANCH_COMMAND = "git branch -M main"

INSTALL_VIRTUALENV_COMMAND = 'python -m pip install virtualenv'
CREAT_VIRTUAL_ENV_COMMAND = 'python -m venv'
# ========================= Default Configuration


# ========================= Default configuration
folder = os.path.dirname(os.path.abspath(__file__))
ASSET_FOLDER = os.path.join(folder, 'source_code_assets')

GIT_IGNORE_FILE = '.gitignore'
GIT_IGNORE_PATH = os.path.join(ASSET_FOLDER, GIT_IGNORE_FILE)

INIT_FILE = '__init__.py'
INIT_FILE_PATH = os.path.join(ASSET_FOLDER, INIT_FILE)

DOT_ENV_FILE = '.env'
DOT_ENV_FILE_PATH = os.path.join(ASSET_FOLDER, DOT_ENV_FILE)

DOT_EXAMPLE_ENV_FILE = '.example.env'
DOT_EXAMPLE_ENV_FILE_PATH = os.path.join(ASSET_FOLDER, DOT_EXAMPLE_ENV_FILE)

REQUIREMENT_FILE = 'requirements.txt'
REQUIREMENT_FILE_PATH = os.path.join(ASSET_FOLDER, REQUIREMENT_FILE)

MAIN_FILE = 'main.py'
MAIN_FILE_PATH = os.path.join(ASSET_FOLDER, MAIN_FILE)

TEST_ALL_FILE = 'test_all.py'
TEST_ALL_FILE_PATH = os.path.join(ASSET_FOLDER, TEST_ALL_FILE)

TEST_UNITTEST_FILE = 'test_unittest.py'
TEST_UNITTEST_FILE_PATH = os.path.join(ASSET_FOLDER, TEST_UNITTEST_FILE)

TEST_FILE = 'test.py'
TEST_FILE_PATH = os.path.join(ASSET_FOLDER, TEST_FILE)

SERVER_FILE = 'server.py'
SERVER_FILE_PATH = os.path.join(ASSET_FOLDER, SERVER_FILE)

CONSTANT_ENV_FILE = 'env.py'
CONSTANT_ENV_FILE_PATH = os.path.join(ASSET_FOLDER, CONSTANT_ENV_FILE)

DATABASE_BASE_FILE = 'base.py'
DATABASE_BASE_FILE_PATH = os.path.join(ASSET_FOLDER, DATABASE_BASE_FILE)
# ========================= Default configuration


# ========================= Default configuration
APP_FOLDER = 'app'
APP_API_FOLDER = os.path.join(APP_FOLDER, 'api')
APP_API_V1_FOLDER = os.path.join(APP_API_FOLDER, 'v1')
APP_CONTROLLER_FOLDER = os.path.join(APP_FOLDER, 'controllers')
APP_SCHEMA_FOLDER = os.path.join(APP_FOLDER, 'schemas')
APP_UTIL_FOLDER = os.path.join(APP_FOLDER, 'utils')

TEST_FOLDER = 'tests'

CONSTANTS_FOLDER = 'constants'

DATABASE_FOLDER = 'databases'
DATABASE_MODEL_FOLDER = os.path.join(DATABASE_FOLDER, 'models')
# ========================= Default configuration