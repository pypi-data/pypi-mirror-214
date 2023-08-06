import os

from .command_line import *
from .ntt_argparser import *
from ..constants import *


class VirtualEnv:
    @classmethod
    def setup(cls, folder_name: str) -> None:
        print("Here")
        venv_path = os.path.join(NTTArgparser.parser.get_project_name(), folder_name)
        commands = [
            INSTALL_VIRTUALENV_COMMAND,
            f"{CREAT_VIRTUAL_ENV_COMMAND} {venv_path}",
        ]

        for command in commands:
            NTTCommandLine.run_command(
                command=command
            )

    @classmethod
    def install_package(cls, package: str = None, requirement: str = None) -> None:
        python_exe = os.path.join(
            NTTArgparser.parser.get_project_name(), DEAFULT_VENV_PYTHON_EXE)

        if package is not None:
            NTTCommandLine.run_command(
                command=f"{python_exe} -m pip install {package}"
            )
        elif requirement is not None:
            NTTCommandLine.run_command(
                command=f"{python_exe} -m pip install -r {requirement}"
            )