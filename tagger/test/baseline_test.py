import unittest2
from StringIO import StringIO

import mock
from mock import MagicMock, patch

from .. import baseline

class BaselineTest(unittest2.TestCase):
    def setUp(self):
        self._tags = {"a":{"NN": 1, "NNP": 2},
                "b":{"MD": 2, "VB":1}}

    def test_baseline_tags(self):
        expected_tagging = {"a": "NNP", "b": "MD"}
        expected_tag  = "MD"
        actual_tag, actual_tagging = baseline.get_baseline_tags(self._tags)

        self.assertEqual(expected_tagging, actual_tagging)
        self.assertEqual(expected_tag, actual_tag)

    def test_parse_train_data(self):
        lines = """NNP a
        NN a
        MD b
        VB b
        MD b
        NNP a"""

        m = mock_open(data=StringIO(lines))
        open_name = "{0}.open".format(baseline.__name__)
        filename = ""

        with patch(open_name, m, create=True):
            actual = baseline.parse_train_data(filename)

        self.assertEqual(self._tags, actual)

    def test_write_test_tags(self):
        tagged = {"a": "NN", "b": "MD"}
        lines = ["a", "b", "c"]

        m = mock_open()
        open_name = "{0}.open".format(baseline.__name__)
        filename = ""
        default_tag = "NNP"

        expected_calls = [mock.call().write("NN a\n"),
                mock.call().write("MD b\n"),
                mock.call().write("{0} c\n".format(default_tag))]


        with patch(open_name, m, create=True):
            baseline.write_test_tags(default_tag, tagged, lines, filename)

        self.assertListEqual(m.mock_calls[2:-1], expected_calls)


# Shamelessly copied from Mock website:
# http://www.voidspace.org.uk/python/mock/examples.html#mocking-open
def mock_open(mock=None, data=None):
    file_spec = file
    if mock is None:
        mock = MagicMock(spec=file_spec)

    handle = MagicMock(spec=file_spec)
    handle.write.return_value = None
    if data is None:
        handle.__enter__.return_value = handle
    else:
        handle.__enter__.return_value = data
    mock.return_value = handle
    return mock

