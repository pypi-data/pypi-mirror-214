from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nanochain",
    version="0.3",
    author="Troy (Guodong) Zhao",
    author_email="gzhao1997@gmail.com",
    description="NanoChain is a Python library designed to provide a suite of useful tools for text processing, vector indexing, and utilizing OpenAI's GPT API to perform various tasks. This is a minimalistic implementation of LangChain because it's too complicated and difficult to customize.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Troyanovsky/nano_chain",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "openai",
        "demjson3",
        "tiktoken",
        "chromadb",
        "PyPDF2",
    ],
)
