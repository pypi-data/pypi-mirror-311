from setuptools import setup, find_packages
from pathlib import Path

# Lire le README avec le bon encodage
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="modern-logger",
    version="0.1.0",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "rich",
        "pyyaml",
        "pydantic",
        "uvicorn",
        "aiohttp",
        "asyncio",
    ],
    author="BANAS Yann",
    author_email="yannbanas@gmail.com",
    description="Advanced logging system with real-time streaming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)