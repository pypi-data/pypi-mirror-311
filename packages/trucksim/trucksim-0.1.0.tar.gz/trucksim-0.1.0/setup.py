
from setuptools import setup, find_packages

setup(
    name="trucksim",
    version="0.1.0",
    description="Virtual CAN simulation package for educational use",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/trucksim",
    packages=find_packages(),
    install_requires=[
        "python-can",
    ],
    entry_points={
        "console_scripts": [
            "cansend=trucksim.cli.cansend:main",
            "cangen=trucksim.cli.cangen:main",
            "candump=trucksim.cli.candump:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
