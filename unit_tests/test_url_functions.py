import unittest
from unittest.mock import patch, MagicMock
from functions.url_functions import read_text_from_url, online_search

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

    @patch('functions.url_functions.search')
    def test_online_search(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        result = online_search('test query')
        self.assertIn('http://example1.com', result)
        self.assertIn('http://example2.com', result)

if __name__ == '__main__':
    unittest.main()