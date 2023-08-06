import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="erniechatbotsdk",
    version="0.0.7",
    description="Baidu Wenxin word api package",
    author="Tk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="tkzhu66@gmail.com",
    packages=find_packages(),
    install_requires=[
        "wcwidth"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)