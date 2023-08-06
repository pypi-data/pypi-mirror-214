# ------------ path configuration ------------- 
import sys
sys.path.append('nttfastapi')
sys.path.append('nttfastapi/utils')
# ------------ path configuration ------------- 

# ------------ python package ------------- 
import unittest
from unittest.mock import *
from argparse import Namespace
# ------------ python package ------------- 

# ------------ project package ------------
from nttfastapi.utils import *
from nttfastapi.constants import *
from tests.constants import *
# ------------ project package ------------


class TestNTTArgparser(unittest.TestCase):
    def setUp(self) -> None:
        NTTArgparser()

        self.action_func = Mock()
        NTTArgparser.parser.add_action(action_name=CREATE_ACTION_NAME, args={
            NTTArgparser.PROJECT_NAME_KEY: DEFAULT_PROJECT_FOLDER,
        }, action=self.action_func)


    @patch('argparse.ArgumentParser.parse_args', 
           return_value=Namespace(
                **{
                    NTTArgparser.ACTION_KEY: CREATE_ACTION_NAME, 
                    NTTArgparser.PROJECT_NAME_KEY: TEST_PROJECT_NAME
                }))
    def test_create_configuration_with_first_action(self, mock_arg_parser):
        NTTArgparser.parser.run()

        self.action_func.assert_called()
        self.assertTrue(
            TEST_PROJECT_NAME in self.action_func.call_args.args
        )

        self.assertEqual(
            NTTArgparser.parser.get_project_name(),
            TEST_PROJECT_NAME
        )