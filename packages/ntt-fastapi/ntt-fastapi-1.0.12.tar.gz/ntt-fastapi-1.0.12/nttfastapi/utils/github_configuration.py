from .file_system import *
from .command_line import *
from .ntt_argparser import *
from ..constants import *


class GithubConfiguration:
    @classmethod
    def setup(cls) -> None:
        git_commands = [
            INIT_GIT_COMMAND,
            ADD_ALL_TO_GIT_COMMAND,
            FIRST_COMMIT_COMMAND,
            # CREATE_BRANCH_COMMAND,
        ]

        folder_path = NTTArgparser.parser.get_project_name()

        for command in git_commands:
            NTTCommandLine.run_command(
                command=command,
                folder_path=folder_path
            )

        NTTFileSystem.clone_file(
            src_path=GIT_IGNORE_PATH, 
            des_path=os.path.join(
                NTTArgparser.parser.get_project_name(),
                GIT_IGNORE_FILE
            ))