from setuptools import setup, find_packages

setup(
    name="gpt-context-builder",
    version="0.1.0",
    description="A tool for creating context blocks for ChatGPT from local files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="masuidrive",
    author_email="masuidrive@masuidrive.jp",
    url="https://github.com/masuidrive/gpt-context-builder",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=2.0.0",
        "pathspec>=0.9.0",
        "tiktoken>=0.3.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gpt-context-builder=gpt_context_builder.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
)
