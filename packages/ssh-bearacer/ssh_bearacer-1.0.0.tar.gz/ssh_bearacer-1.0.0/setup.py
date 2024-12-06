from setuptools import setup, find_packages

setup(
    name="ssh-bearacer",
    version="1.0.0",
    description="A library for managing SSH connections and deployments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Duy Nguyen Ngoc",
    author_email="duynn100198@gmail.com",
    url="https://github.com/olololoe110399/ssh-deployer",
    packages=find_packages(),
    install_requires=[
        "paramiko",
        "sshtunnel",
    ],
    entry_points={
        "console_scripts": [
            "ssh-deployer=ssh_deployer.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
