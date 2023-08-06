import argparse
from typing import *

from ..constants import *


class NTTArgparser:
    ACTION_KEY = 'action'
    PROJECT_NAME_KEY = 'project_name'

    parser = None

    def __init__(self) -> None:
        NTTArgparser.parser = self
        self.__action_list = []
        self.__project_name = None
        self.__action_dict = {}

    def add_action(self, 
                   action_name: str, 
                   args: Dict[str, object], 
                   action: Callable[..., Any]) -> None:
        self.__action_list.append(action_name)

        if NTTArgparser.PROJECT_NAME_KEY in args:
            self.__project_name = args[NTTArgparser.PROJECT_NAME_KEY]
        self.__action_dict[action_name] = action

    def get_project_name(self) -> str:
        return self.__project_name

    def run(self) -> None:
        parser = argparse.ArgumentParser()

        parser.add_argument(NTTArgparser.ACTION_KEY, choices=self.__action_list)
        parser.add_argument(f"--{NTTArgparser.PROJECT_NAME_KEY}", default=DEFAULT_PROJECT_FOLDER)

        args = parser.parse_args()

        self.__project_name = getattr(args, NTTArgparser.PROJECT_NAME_KEY)

        self.__action_dict[getattr(args, NTTArgparser.ACTION_KEY)](self.__project_name)