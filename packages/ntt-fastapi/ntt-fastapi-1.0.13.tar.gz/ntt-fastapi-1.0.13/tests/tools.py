from unittest.mock import *

from nttfastapi.utils import *


def mock_project_name(project_name):
    parser_mock = Mock(spec=NTTArgparser)
    parser_mock.get_project_name.return_value = project_name
    NTTArgparser.parser = parser_mock