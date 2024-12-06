# textfromimage/azure_openai.py
import os
from typing import List, Optional, Dict, Union
from openai import AzureOpenAI
from .utils import get_image_data, process_batch_images, BatchResult

_client = None
_deployment_name = None


def init(
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        deployment_name: Optional[str] = None,
        api_version: str = "2024-02-15-preview"
) -> None:
    """Initialize Azure OpenAI client."""
    global _client, _deployment_name

    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    api_base = api_base or os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not all([api_key, api_base, deployment_name]):
        raise ValueError(
            "Azure OpenAI configuration must be provided either via parameters or environment variables:\n"
            "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT"
        )

    # Ensure api_base has the correct format
    if not api_base.endswith('/'):
        api_base += '/'

    _client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        base_url=f"{api_base}openai/deployments/{deployment_name}"
    )
    _deployment_name = deployment_name


def get_description(
        image_path: str,
        prompt: str = "What's in this image?",
        max_tokens: int = 300,
        system_prompt: str = "You are a helpful assistant."
) -> str:
    """Get image description using Azure OpenAI's vision capabilities."""
    if _client is None:
        init()

    encoded_image, _ = get_image_data(image_path)

    try:
        response = _client.chat.completions.create(
            model=_deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Azure OpenAI API request failed: {str(e)}")


def get_description_batch(
        image_paths: List[str],
        prompt: str = "What's in this image?",
        max_tokens: int = 300,
        system_prompt: str = "You are a helpful assistant.",
        concurrent_limit: int = 3
) -> List[BatchResult]:
    """Process multiple images in batch."""
    if _client is None:
        init()

    return process_batch_images(
        image_paths=image_paths,
        processor=get_description,
        concurrent_limit=concurrent_limit,
        prompt=prompt,
        max_tokens=max_tokens,
        system_prompt=system_prompt
    )
