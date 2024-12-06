# textfromimage/__init__.py
from . import openai
from . import azure_openai
from . import claude
from .utils import BatchResult  # Added BatchResult for easy access

__all__ = ['openai', 'azure_openai', 'claude', 'BatchResult']
