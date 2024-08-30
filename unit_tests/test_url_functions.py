import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import functions

read_text_from_url = getattr(functions, "read_text_from_url")
online_search = getattr(functions, "online_search")

class TestUrlFunctions(unittest.TestCase):

    @patch('urllib.request.urlopen')
    @patch('bs4.BeautifulSoup')
    def test_read_text_from_url(self, mock_bs4, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body><p>Hello World</p></body></html>'
        mock_urlopen.return_value = mock_response
        
        mock_bs4.return_value.get_text.return_value = 'Hello World'
        
        result = read_text_from_url('http://example.com')
        self.assertEqual(result, 'Hello World')

    def test_online_search(self):
        result = online_search('google')
        self.assertIn("https://en.wikipedia.org/wiki/Google", result)

if __name__ == '__main__':
    unittest.main()