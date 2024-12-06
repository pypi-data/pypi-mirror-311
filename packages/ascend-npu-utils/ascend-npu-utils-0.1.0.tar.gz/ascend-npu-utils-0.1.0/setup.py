
from setuptools import setup, find_packages

setup(
    name='ascend-npu-utils',  # Name of your package
    version='0.1.0',  # Initial version number
    author='Harsh',  # Your name
    description='A utility library for interacting with Ascend NPUs via the npu-smi command options, to directly get information from the terminal commands parsed into python',  # Brief description of your package
    long_description=open('README.md').read(),  # Detailed description read from README.md
    long_description_content_type='text/markdown',  # Format of the long description
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[  # List of dependencies required for your package
        'psutil',  # Dependency for system and process utilities
    ],
    classifiers=[  # Metadata to categorize your package
        'Programming Language :: Python :: 3',  # Supported Python version
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # OS compatibility
    ],
    python_requires='>=3.6',  # Minimum required Python version
)
