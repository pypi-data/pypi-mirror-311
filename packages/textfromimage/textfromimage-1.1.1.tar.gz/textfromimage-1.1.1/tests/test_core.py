# tests/test_core.py
import unittest
from unittest.mock import patch, MagicMock
import os
from textfromimage import openai as openai_module
from textfromimage import azure_openai as azure_openai_module
from textfromimage import claude as claude_module
from textfromimage.utils import BatchResult


class TestUtils(unittest.TestCase):
    """Tests for the utility functions."""

    @patch('textfromimage.utils.requests.get')
    def test_get_image_data_url(self, mock_requests_get):
        """Test getting image data from URL."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        encoded_image, content_type = openai_module.get_image_data('https://example.com/image.jpg')
        self.assertIsInstance(encoded_image, str)
        self.assertEqual(content_type, 'image/jpeg')

    @patch('textfromimage.utils.os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'test_image_content')
    def test_get_image_data_local(self, mock_open, mock_exists):
        """Test getting image data from local file."""
        mock_exists.return_value = True

        encoded_image, content_type = openai_module.get_image_data('/path/to/local/image.jpg')
        self.assertIsInstance(encoded_image, str)
        self.assertEqual(content_type, 'image/jpeg')
        mock_open.assert_called_once_with('/path/to/local/image.jpg', 'rb')

    def test_get_image_data_invalid_local(self):
        """Test getting image data from non-existent local file."""
        with self.assertRaises(ValueError):
            openai_module.get_image_data('/nonexistent/path/image.jpg')


class TestOpenAI(unittest.TestCase):
    """Tests for the OpenAI backend of TextFromImage."""

    # [Previous OpenAI tests remain the same]

    @patch('textfromimage.openai.requests.get')
    @patch('textfromimage.openai.OpenAI')
    def test_batch_processing(self, mock_openai_client, mock_requests_get):
        """Test batch processing of images."""
        # Mock HTTP responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        # Mock OpenAI responses
        mock_chat = MagicMock()
        mock_chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test description"))]
        )
        mock_openai_client.return_value = MagicMock(chat=mock_chat)

        # Initialize client
        openai_module.init(api_key="dummy_openai_api_key")

        # Test batch processing
        image_paths = [
            'https://example.com/image1.jpg',
            '/path/to/local/image2.jpg',
            'https://example.com/image3.jpg'
        ]

        results = openai_module.get_description_batch(image_paths)

        self.assertEqual(len(results), 3)
        self.assertIsInstance(results[0], BatchResult)
        self.assertTrue(results[0].success)
        self.assertEqual(results[0].description, "Test description")

    def test_batch_size_limit(self):
        """Test batch size limit enforcement."""
        openai_module.init(api_key="dummy_openai_api_key")

        too_many_images = ['image.jpg'] * 21
        with self.assertRaises(ValueError) as context:
            openai_module.get_description_batch(too_many_images)
        self.assertIn("Maximum of 20 images", str(context.exception))


class TestAzureOpenAI(unittest.TestCase):
    """Tests for the Azure OpenAI backend of TextFromImage."""

    # [Previous Azure OpenAI tests remain the same]

    @patch('textfromimage.azure_openai.requests.get')
    @patch('textfromimage.azure_openai.AzureOpenAI')
    def test_batch_processing(self, mock_azure_client, mock_requests_get):
        """Test batch processing of images with Azure OpenAI."""
        # Mock setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        mock_chat = MagicMock()
        mock_chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test description from Azure"))]
        )
        mock_azure_client.return_value = MagicMock(chat=mock_chat)

        # Initialize client
        azure_openai_module.init(
            api_key="dummy_azure_api_key",
            api_base="https://dummy-azure-endpoint.openai.azure.com/",
            deployment_name="dummy-deployment"
        )

        # Test batch processing
        image_paths = [
            'https://example.com/image1.jpg',
            '/path/to/local/image2.jpg'
        ]

        results = azure_openai_module.get_description_batch(
            image_paths,
            system_prompt="Custom system prompt",
            concurrent_limit=2
        )

        self.assertEqual(len(results), 2)
        self.assertTrue(all(result.success for result in results))
        self.assertEqual(results[0].description, "Test description from Azure")


class TestClaude(unittest.TestCase):
    """Tests for the Anthropic Claude backend of TextFromImage."""

    # [Previous Claude tests remain the same]

    @patch('textfromimage.claude.requests.get')
    @patch('textfromimage.claude.Anthropic')
    def test_batch_processing(self, mock_claude_client, mock_requests_get):
        """Test batch processing of images with Claude."""
        # Mock setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/jpeg'}
        mock_response.content = b'test_image_content'
        mock_requests_get.return_value = mock_response

        mock_messages = MagicMock()
        mock_messages.create.return_value = MagicMock(
            content=[MagicMock(text="Test description from Claude")]
        )
        mock_claude_client.return_value = MagicMock(messages=mock_messages)

        # Initialize client
        claude_module.init(api_key="dummy_claude_api_key")

        # Test batch processing
        image_paths = [
            'https://example.com/image1.jpg',
            '/path/to/local/image2.jpg',
            'https://example.com/image3.jpg'
        ]

        results = claude_module.get_description_batch(
            image_paths,
            model="claude-3-sonnet-20240229",
            concurrent_limit=3
        )

        self.assertEqual(len(results), 3)
        self.assertTrue(all(result.success for result in results))
        self.assertEqual(results[0].description, "Test description from Claude")

    def test_media_type_validation(self):
        """Test media type validation for Claude."""
        claude_module.init(api_key="dummy_claude_api_key")

        test_cases = [
            ('image.jpg', 'image/jpeg'),
            ('image.jpeg', 'image/jpeg'),
            ('image.png', 'image/png'),
            ('image.gif', 'image/gif'),
            ('image.webp', 'image/webp'),
            ('image.unknown', 'image/jpeg')  # Default fallback
        ]

        for filename, expected_type in test_cases:
            with patch('textfromimage.utils.os.path.exists', return_value=True), \
                    patch('builtins.open', unittest.mock.mock_open(read_data=b'test')):
                _, content_type = claude_module.get_image_data(filename)
                self.assertEqual(content_type, expected_type)


if __name__ == '__main__':
    unittest.main()