from setuptools import setup, find_packages

setup(
    name="textual_watch",
    version="0.0.1",
    description="Widget for Textual to watch a shell command",
    url="https://github.com/BlakeJC94/textual-watch",
    author="BlakeJC94",
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "textual",
    ],
)
