import pytest
from unittest.mock import patch, Mock
from client import ApiClient
from core.models.movie import Movie
from core.models.quote import Quote
from core.utils.errors import AuthenticationError

# Test if the client is correctly initialized.
def test_init_client():
    client = ApiClient('https://test.com', 'test_api_key')

    assert client.base_url == 'https://test.com'
    assert client.api_key == 'test_api_key'
    assert isinstance(client.movie, Movie)
    assert isinstance(client.quote, Quote)

# Test if the function create_session is raising an error when the API key is None or not a string.
@patch('client.Session')
def test_create_session(mock_session):
    client = ApiClient('https://test.com', 'test_api_key')

    assert client.session is not None
    mock_session.assert_called_once()
    mock_session.return_value.headers.update.assert_called_once_with({'Authorization': 'Bearer test_api_key'})

# Test if the function create_session is raising an error when the API key is None.
def test_create_session_no_key():
    with pytest.raises(ValueError):
        client = ApiClient('https://test.com', None)