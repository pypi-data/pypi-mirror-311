# textfromimage/openai.py
import os
from typing import List, Optional
from openai import OpenAI
from .utils import get_image_data, process_batch_images, BatchResult

_client = None


def init(api_key: Optional[str] = None) -> None:
    """
    Initialize OpenAI client with API key.

    Parameters:
    - api_key (str, optional): OpenAI API key. If not provided, reads from OPENAI_API_KEY env var.
    """
    global _client
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key must be provided via api_key parameter or OPENAI_API_KEY environment variable.")
    _client = OpenAI(api_key=api_key)


def get_description(
        image_path: str,
        prompt: str = "What's in this image?",
        max_tokens: int = 300,
        model: str = "gpt-4-vision-preview"
) -> str:
    """
    Get image description using OpenAI's vision models.

    Parameters:
    - image_path (str): URL or local path of the image to analyze
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - model (str): OpenAI model to use

    Returns:
    - str: Generated description
    """
    if _client is None:
        init()

    encoded_image, _ = get_image_data(image_path)

    try:
        response = _client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenAI API request failed: {str(e)}")


def get_description_batch(
        image_paths: List[str],
        prompt: str = "What's in this image?",
        max_tokens: int = 300,
        model: str = "gpt-4-vision-preview",
        concurrent_limit: int = 3
) -> List[BatchResult]:
    """
    Process multiple images in batch.

    Parameters:
    - image_paths (List[str]): List of image URLs or local paths
    - prompt (str): Prompt for the model
    - max_tokens (int): Maximum response length
    - model (str): OpenAI model to use
    - concurrent_limit (int): Maximum number of concurrent operations

    Returns:
    - List[BatchResult]: Results for each image
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