# ------------ python package ------------- 
import os
import sys 
sys.path.append('nttfastapi')
# ------------ python package ------------- 

# ------------ project package ------------
from .utils import *
from .constants import *
# ------------ project package ------------


def main():
    parser = NTTArgparser()

    parser.add_action(
        action_name=CREATE_ACTION_NAME,
        args={
            NTTArgparser.PROJECT_NAME_KEY: DEFAULT_PROJECT_FOLDER,
        },
        action=create_folder_action,
    )

    parser.add_action(
        action_name='test',
        args={},
        action=test_function,
    )

    parser.run()

def test_function(*args, **kwargs):
    print("Testing")


def create_folder_action(folder_name: str):
    NTTFileSystem.create_folder(folder_name=folder_name)
    VirtualEnv.setup(folder_name=DEFAULT_VENV_FOLDER)
    ProjectConfiguration.setup()
    GithubConfiguration.setup()


if __name__ == "__main__":
    main()