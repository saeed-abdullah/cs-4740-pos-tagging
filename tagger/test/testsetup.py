# Sets up the mock_open

from mock import MagicMock

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

