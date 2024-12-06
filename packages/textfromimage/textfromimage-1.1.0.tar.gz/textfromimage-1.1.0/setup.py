from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="textfromimage",
    version="1.1.0",
    author="Oren Grinker",
    author_email="orengr4@gmail.com",
    description="Get descriptions of images from OpenAI, Azure OpenAI, and Anthropic Claude models with support for local files and batch processing.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/OrenGrinker/textfromimage",
    packages=find_packages(),
    install_requires=[
        "openai>=1.35.15",
        "requests>=2.25.1",
        "anthropic>=0.18.1",
        "typing-extensions>=4.5.0",
    ],
    extras_require={
        "azure": ["azure-identity>=1.15.0"],
        "all": [
            "azure-identity>=1.15.0",
            "aiohttp>=3.8.0",
            "python-magic>=0.4.27"  # For better file type detection
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires='>=3.9',
    keywords=[
        "openai",
        "gpt-4",
        "claude",
        "azure-openai",
        "computer-vision",
        "image-to-text",
        "ai",
        "machine-learning",
        "batch-processing",
        "local-files",
        "image-analysis",
        "vision-ai"
    ],
    project_urls={
        'Bug Reports': 'https://github.com/OrenGrinker/textfromimage/issues',
        'Source': 'https://github.com/OrenGrinker/textfromimage',
    },
)