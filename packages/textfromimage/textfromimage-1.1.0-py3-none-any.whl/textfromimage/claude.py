# textfromimage/claude.py
import os
from typing import List, Optional
from anthropic import Anthropic
from .utils import get_image_data, process_batch_images, BatchResult, get_valid_media_type

_client = None


def init(api_key: Optional[str] = None) -> None:
    """
    Initialize Claude client with API key.

    Parameters:
    - api_key (str, optional): Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var.
    """
    global _client
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "Anthropic API key must be provided via api_key parameter or ANTHROPIC_API_KEY environment variable.")
    _client = Anthropic(api_key=api_key)


def get_description(
        image_path: str,
        prompt: str = "What's in this image?",
        max_tokens: int = 300,
        model: str = "claude-3-sonnet-20240229"
) -> str:
    """
    Get image description using Claude's vision capabilities.

    Parameters:
    - image_path (str): URL or local file path of the image to analyze
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - model (str): Claude model to use
        Available models:
        - claude-3-opus-20240229
        - claude-3-sonnet-20240229
        - claude-3-haiku-20240229

    Returns:
    - str: Generated description

    Raises:
    - ValueError: If image cannot be loaded or processed
    - RuntimeError: If API request fails
    """
    if _client is None:
        init()

    try:
        encoded_image, content_type = get_image_data(image_path)
        # Ensure media type is valid for Claude
        media_type = get_valid_media_type(content_type)

        response = _client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        if not response.content or not response.content[0].text:
            raise RuntimeError("No response content received from Claude")

        return response.content[0].text
    except ValueError as e:
        # Re-raise ValueError for image processing errors
        raise
    except Exception as e:
        raise RuntimeError(f"Claude API request failed: {str(e)}")


def get_description_batch(
        image_paths: List[str],
        prompt: str = "What's in this image?",
        max_tokens: int = 300,
        model: str = "claude-3-sonnet-20240229",
        concurrent_limit: int = 3
) -> List[BatchResult]:
    """
    Process multiple images in batch using Claude's vision capabilities.

    Parameters:
    - image_paths (List[str]): List of image URLs or local file paths
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - model (str): Claude model to use
    - concurrent_limit (int): Maximum number of concurrent operations

    Returns:
    - List[BatchResult]: List of results for each image, containing:
        - success (bool): Whether processing was successful
        - description (Optional[str]): Generated description if successful
        - error (Optional[str]): Error message if processing failed
        - image_path (str): Original image path

    Raises:
    - ValueError: If too many images are provided (>20)
    - RuntimeError: If client is not initialized
    """
    if _client is None:
        init()

    return process_batch_images(
        image_paths=image_paths,
        processor=get_description,
        concurrent_limit=concurrent_limit,
        prompt=prompt,
        max_tokens=max_tokens,
        model=model
    )


def is_initialized() -> bool:
    """
    Check if the Claude client is initialized.

    Returns:
    - bool: True if client is initialized, False otherwise
    """
    return _client is not None


def get_supported_models() -> List[str]:
    """
    Get list of supported Claude model versions.

    Returns:
    - List[str]: List of supported model identifiers
    """
    return [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240229"
    ]