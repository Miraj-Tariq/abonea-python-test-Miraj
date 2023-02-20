import logging
import unittest
from unittest.mock import patch, MagicMock

from backend.utils.decorators import retry
from backend.utils.request import api_request


class TestApiRequest(unittest.TestCase):
    @patch("backend.utils.request.requests.get")
    def test_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response

        result = api_request("https://example.com/api")
        self.assertEqual(result, {"success": True})

    def test_url_variables(self):
        with patch("backend.utils.request.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"success": True}
            mock_get.return_value = mock_response

            api_request("https://example.com/api", foo="bar", baz="qux")
            mock_get.assert_called_with("https://example.com/api?foo=bar&baz=qux")

    def test_no_url_variables(self):
        with patch("backend.utils.request.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"success": True}
            mock_get.return_value = mock_response

            api_request("https://example.com/api")
            mock_get.assert_called_with("https://example.com/api")
