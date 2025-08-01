import unittest
from unittest.mock import patch, Mock, call
from datetime import datetime
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage.storagemanager import storeData, getNewListings, COLLECTION_NAME


class TestStorageManager(unittest.TestCase):
    
    @patch('storage.storagemanager.getMongoCollection')
    @patch('storage.storagemanager.datetime')
    def test_storeData(self, mock_datetime, mock_getMongoCollection):
        """Test that storeData processes data and performs bulk write operations"""
        # Mock datetime.utcnow()
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = mock_now
        
        # Mock collection
        mock_collection = Mock()
        mock_getMongoCollection.return_value = mock_collection
        
        # Sample data (format: [rank, ?, code, company, price, change, percentage_change, market_cap, year_percentage_change])
        test_data = [
            ['1', 'ASX', 'ASX', 'ASX Limited', '$65.50', '+1.20', '+1.87%', '$7.1B', '+15.2%'],
            ['2', 'CBA', 'CBA', 'Commonwealth Bank', '$105.20', '-0.50', '-0.47%', '$180.5B', '+8.5%']
        ]
        
        # Call the function
        storeData(test_data)
        
        # Verify collection was obtained
        mock_getMongoCollection.assert_called_once_with(COLLECTION_NAME)
        
        # Verify bulk_write was called
        mock_collection.bulk_write.assert_called_once()
        
        # Get the operations passed to bulk_write
        call_args = mock_collection.bulk_write.call_args[0][0]
        self.assertEqual(len(call_args), 2)  # Should have 2 operations
        
        # Verify the structure of the operations (they should be UpdateOne operations)
        from pymongo import UpdateOne
        for op in call_args:
            self.assertIsInstance(op, UpdateOne)
    
    @patch('storage.storagemanager.getMongoCollection')
    def test_storeData_empty_data(self, mock_getMongoCollection):
        """Test that storeData handles empty data correctly"""
        mock_collection = Mock()
        mock_getMongoCollection.return_value = mock_collection
        
        # Call with empty data
        storeData([])
        
        # Verify collection was obtained
        mock_getMongoCollection.assert_called_once_with(COLLECTION_NAME)
        
        # Verify bulk_write was called with empty operations
        mock_collection.bulk_write.assert_called_once_with([])
    
    @patch('storage.storagemanager.getMongoCollection')
    def test_getNewListings(self, mock_getMongoCollection):
        """Test that getNewListings queries for new listings correctly"""
        # Mock collection and results
        mock_collection = Mock()
        mock_results = [
            {'Code': 'ASX', 'Company': 'ASX Limited', 'Discovered_At': datetime(2023, 1, 1, 10, 0, 0)},
            {'Code': 'CBA', 'Company': 'Commonwealth Bank', 'Discovered_At': datetime(2023, 1, 1, 11, 0, 0)}
        ]
        mock_collection.find.return_value = mock_results
        mock_getMongoCollection.return_value = mock_collection
        
        # Test date
        start_date = datetime(2023, 1, 1, 9, 0, 0)
        
        # Call the function
        result = getNewListings(start_date)
        
        # Verify collection was obtained
        mock_getMongoCollection.assert_called_once_with(COLLECTION_NAME)
        
        # Verify find was called with correct query
        expected_query = {'Discovered_At': {'$gte': start_date}}
        mock_collection.find.assert_called_once_with(expected_query)
        
        # Verify result
        self.assertEqual(result, mock_results)
    
    @patch('storage.storagemanager.getMongoCollection')
    def test_getNewListings_no_results(self, mock_getMongoCollection):
        """Test that getNewListings handles no results correctly"""
        mock_collection = Mock()
        mock_collection.find.return_value = []
        mock_getMongoCollection.return_value = mock_collection
        
        start_date = datetime(2023, 1, 1, 9, 0, 0)
        
        result = getNewListings(start_date)
        
        # Verify empty result
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()