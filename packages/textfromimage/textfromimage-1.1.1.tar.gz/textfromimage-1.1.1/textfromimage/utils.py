# textfromimage/utils.py
import os
import base64
import requests
import mimetypes
import asyncio
from typing import List, Dict, Union, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


@dataclass
class BatchResult:
    """Result of processing a single image in a batch."""
    success: bool
    description: Optional[str]
    error: Optional[str]
    image_path: str


def get_valid_media_type(content_type: str) -> str:
    """Validate and normalize media type."""
    valid_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    normalized_type = content_type.lower()

    if normalized_type in valid_types:
        return normalized_type
    if normalized_type == 'image/jpg':
        return 'image/jpeg'
    return 'image/jpeg'


def get_image_data(image_path: str) -> Tuple[str, str]:
    """
    Process image from URL or local file path.
    Returns base64 encoded image and content type.

    Parameters:
    - image_path: URL or local file path to the image

    Returns:
    - Tuple[str, str]: (base64 encoded image, content type)
    """

    def is_url(path: str) -> bool:
        return path.startswith(('http://', 'https://'))

    try:
        if is_url(image_path):
            response = requests.get(image_path)
            if response.status_code != 200:
                raise ValueError(f"Could not retrieve image from URL: {image_path}")

            # Get content type from response or guess from URL
            content_type = response.headers.get('content-type')
            if not content_type:
                content_type, _ = mimetypes.guess_type(image_path)
            content_type = get_valid_media_type(content_type or 'image/jpeg')

            encoded_image = base64.b64encode(response.content).decode('utf-8')
        else:
            # Handle local file
            if not os.path.exists(image_path):
                raise ValueError(f"Local file not found: {image_path}")

            # Guess content type from file extension
            content_type, _ = mimetypes.guess_type(image_path)
            content_type = get_valid_media_type(content_type or 'image/jpeg')

            with open(image_path, 'rb') as f:
                image_data = f.read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')

        return encoded_image, content_type
    except Exception as e:
        if is_url(image_path):
            raise ValueError(f"Failed to fetch image from URL: {str(e)}")
        else:
            raise ValueError(f"Failed to read local image: {str(e)}")


def process_batch_images(
        image_paths: List[str],
        processor: callable,
        concurrent_limit: int = 3,
        **kwargs
) -> List[BatchResult]:
    """
    Process multiple images concurrently.

    Parameters:
    - image_paths: List of image URLs or file paths
    - processor: Function to process each image
    - concurrent_limit: Maximum number of concurrent operations
    - kwargs: Additional arguments to pass to the processor

    Returns:
    - List[BatchResult]: Results for each image
    """
    if len(image_paths) > 20:
        raise ValueError("Maximum of 20 images allowed per batch request")

    def process_single(image_path: str) -> BatchResult:
        try:
            description = processor(image_path, **kwargs)
            return BatchResult(
                success=True,
                description=description,
                error=None,
                image_path=image_path
            )
        except Exception as e:
            return BatchResult(
                success=False,
                description=None,
                error=str(e),
                image_path=image_path
            )

    with ThreadPoolExecutor(max_workers=concurrent_limit) as executor:
        results = list(executor.map(process_single, image_paths))

    return results