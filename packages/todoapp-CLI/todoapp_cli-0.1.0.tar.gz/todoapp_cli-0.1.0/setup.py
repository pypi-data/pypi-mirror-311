# setup.py

from setuptools import setup, find_packages

setup(
    name="todoapp-CLI",  # Package name
    version="0.1.0",  # Initial version
    description="A simple to-do list CLI app",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Himanshu Kumar Jha",
    author_email="himanshukrjha004@gmail.com",
    url="https://github.com/himanshu-kr-jha",  # Optional: URL for the project
    packages=find_packages(),
    install_requires=[],  # List any dependencies, leave empty if none
    entry_points={
        'console_scripts': [
            'todoapp = todoapp.todo:main',  # Entry point for the CLI
        ],
    },
    classifiers=[  # Optional: Add classifiers for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
