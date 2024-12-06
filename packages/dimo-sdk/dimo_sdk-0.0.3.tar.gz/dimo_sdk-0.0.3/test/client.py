import unittest
from unittest.mock import patch, MagicMock
import requests
from io import BytesIO

from hub.client import Client

TestURL = "http://localhost:8080"

class TestClient(unittest.TestCase):
    
    @patch('requests.post')
    def test_upload_hub(self, mock_post):
        """Test the upload_hub method."""
        # Arrange
        base_url = TestURL
        client = Client(base_url)
        owner = "owner_name_test"
        filename = "example_meme.jpg"
        msg = "This is a test meme"
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"File": filename, "Start": 0, "Size": 19}
        mock_post.return_value = mock_response

        # Act
        result = client.upload_hub(owner, filename, msg)

        # Assert
        mock_post.assert_called_once_with(f"{base_url}/api/upload", 
                                          headers={'Content-Type': 'application/json'},
                                          data='{"Owner": "owner_name", "ID": "example_meme.jpg", "Message": "This is a test meme"}')
        self.assertIsNone(result)
        mock_response.json.assert_called_once()

    @patch('requests.post')
    def test_upload_hub_data(self, mock_post):
        """Test the upload_hub_data method."""
        # Arrange
        base_url = TestURL
        client = Client(base_url)
        owner = "owner_name_data"
        filename = "example_meme.jpg"
        data = b"fake image data"

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"File": filename, "Start": 0, "Size": 19}
        mock_post.return_value = mock_response

        # Act
        result = client.upload_hub_data(owner, filename, data)

        # Assert
        mock_post.assert_called_once_with(f"{base_url}/api/uploadData", 
                                          files={'file': ('example_meme.jpg', BytesIO(data), 'application/octet-stream')},
                                          data={'owner': owner})
        self.assertIsNone(result)
        mock_response.json.assert_called_once()

    @patch('requests.post')
    def test_download_hub_data(self, mock_post):
        """Test the download_hub_data method."""
        # Arrange
        base_url = TestURL
        client = Client(base_url)
        meme_id = "12345"
        owner = "owner_name"

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake image data"
        mock_post.return_value = mock_response

        # Act
        result = client.download_hub_data(meme_id, owner)

        # Assert
        mock_post.assert_called_once_with(f"{base_url}/api/download", 
                                          data='id=12345&owner=owner_name', 
                                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(result, b"fake image data")
        mock_response.content.assert_called_once()

    @patch('requests.post')
    def test_upload_hub_error(self, mock_post):
        """Test the upload_hub method with an error."""
        # Arrange
        base_url = TestURL
        client = Client(base_url)
        owner = "owner_name"
        filename = "example_meme.jpg"
        msg = "This is a test meme"

        # Create a mock response for a failed request
        mock_response = MagicMock()
        mock_response.status_code = 500  # Internal server error
        mock_post.return_value = mock_response

        # Act
        result = client.upload_hub(owner, filename, msg)

        # Assert
        mock_post.assert_called_once_with(f"{base_url}/api/upload", 
                                          headers={'Content-Type': 'application/json'},
                                          data='{"Owner": "owner_name", "ID": "example_meme.jpg", "Message": "This is a test meme"}')
        self.assertIsNone(result)

    @patch('requests.post')
    def test_download_hub_data_error(self, mock_post):
        """Test the download_hub_data method with an error."""
        # Arrange
        base_url = TestURL
        client = Client(base_url)
        meme_id = "12345"
        owner = "owner_name"

        # Create a mock response for a failed request
        mock_response = MagicMock()
        mock_response.status_code = 500  # Internal server error
        mock_post.return_value = mock_response

        # Act
        result = client.download_hub_data(meme_id, owner)

        # Assert
        mock_post.assert_called_once_with(f"{base_url}/api/download", 
                                          data='id=12345&owner=owner_name', 
                                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
