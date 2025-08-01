import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Ingestion.fetcher import getSession, getPageData, getListings


class TestFetcher(unittest.TestCase):
    
    def test_getSession(self):
        """Test that getSession returns a requests.Session with proper User-Agent"""
        session = getSession()
        
        # Check that it returns a requests.Session object
        import requests
        self.assertIsInstance(session, requests.Session)
        
        # Check that User-Agent header is set correctly
        expected_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        self.assertEqual(session.headers['User-Agent'], expected_user_agent)
    
    @patch('Ingestion.fetcher.getSession')
    def test_getPageData(self, mock_getSession):
        """Test that getPageData makes a GET request and returns page content"""
        # Mock the session and its get method
        mock_session = Mock()
        mock_response = Mock()
        mock_response.text = '<html><body>Test content</body></html>'
        mock_session.get.return_value = mock_response
        mock_getSession.return_value = mock_session
        
        # Call the function
        result = getPageData('http://test.com')
        
        # Verify the session was created and get was called
        mock_getSession.assert_called_once()
        mock_session.get.assert_called_once_with('https://www.marketindex.com.au/asx-listed-companies')
        
        # Verify the result
        self.assertEqual(result, '<html><body>Test content</body></html>')
    
    @patch('Ingestion.fetcher.getPageData')
    def test_getListings(self, mock_getPageData):
        """Test that getListings parses HTML and extracts table data correctly"""
        # Mock HTML content with a sample table
        mock_html = '''
        <html>
        <body>
            <table id="asx_sp_table">
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>ASX</td>
                        <td>ASX</td>
                        <td>ASX Limited</td>
                        <td>$65.50</td>
                        <td>+1.20</td>
                        <td>+1.87%</td>
                        <td>$7.1B</td>
                        <td>+15.2%</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>CBA</td>
                        <td>CBA</td>
                        <td>Commonwealth Bank</td>
                        <td>$105.20</td>
                        <td>-0.50</td>
                        <td>-0.47%</td>
                        <td>$180.5B</td>
                        <td>+8.5%</td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
        '''
        mock_getPageData.return_value = mock_html
        
        # Call the function
        result = getListings()
        
        # Verify the function was called
        mock_getPageData.assert_called_once_with('https://www.marketindex.com.au/asx-listed-companies')
        
        # Verify the result structure
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
        # Check first row data
        expected_first_row = ['1', 'ASX', 'ASX', 'ASX Limited', '$65.50', '+1.20', '+1.87%', '$7.1B', '+15.2%']
        self.assertEqual(result[0], expected_first_row)
        
        # Check second row data
        expected_second_row = ['2', 'CBA', 'CBA', 'Commonwealth Bank', '$105.20', '-0.50', '-0.47%', '$180.5B', '+8.5%']
        self.assertEqual(result[1], expected_second_row)
    
    @patch('Ingestion.fetcher.getPageData')
    def test_getListings_empty_table(self, mock_getPageData):
        """Test that getListings handles empty table correctly"""
        # Mock HTML content with empty table
        mock_html = '''
        <html>
        <body>
            <table id="asx_sp_table">
                <tbody>
                </tbody>
            </table>
        </body>
        </html>
        '''
        mock_getPageData.return_value = mock_html
        
        # Call the function
        result = getListings()
        
        # Verify empty result
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()