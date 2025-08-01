import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mongohelper


class TestMongoHelper(unittest.TestCase):
    
    @patch.dict(os.environ, {'asx_db': 'mongodb://test:27017/testdb'})
    @patch('mongohelper.MongoClient')
    def test_getMongoClient_with_env_var(self, mock_mongo_client):
        """Test that getMongoClient returns MongoClient when environment variable is set"""
        mock_client = Mock()
        mock_mongo_client.return_value = mock_client
        
        result = mongohelper.getMongoClient()
        
        # Verify MongoClient was called with correct connection string
        mock_mongo_client.assert_called_once_with('mongodb://test:27017/testdb')
        self.assertEqual(result, mock_client)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_getMongoClient_without_env_var(self):
        """Test that getMongoClient raises exception when environment variable is not set"""
        with self.assertRaises(Exception) as context:
            mongohelper.getMongoClient()
        
        self.assertEqual(str(context.exception), 'Please set asx_db connection value for mongodb.')
    
    @patch('mongohelper.getMongoClient')
    def test_getMongoDB(self, mock_getMongoClient):
        """Test that getMongoDB returns database from client"""
        mock_client = Mock()
        mock_database = Mock()
        mock_client.get_database.return_value = mock_database
        mock_getMongoClient.return_value = mock_client
        
        result = mongohelper.getMongoDB()
        
        # Verify client was obtained and get_database was called
        mock_getMongoClient.assert_called_once()
        mock_client.get_database.assert_called_once()
        self.assertEqual(result, mock_database)
    
    @patch('mongohelper.getMongoDB')
    def test_getMongoCollection(self, mock_getMongoDB):
        """Test that getMongoCollection returns collection from database"""
        mock_database = Mock()
        mock_collection = Mock()
        # Configure the mock to support dictionary-like access
        mock_database.__getitem__ = Mock(return_value=mock_collection)
        mock_getMongoDB.return_value = mock_database
        
        result = mongohelper.getMongoCollection('test_collection')
        
        # Verify database was obtained and collection was accessed
        mock_getMongoDB.assert_called_once()
        mock_database.__getitem__.assert_called_once_with('test_collection')
        self.assertEqual(result, mock_collection)


if __name__ == '__main__':
    unittest.main()