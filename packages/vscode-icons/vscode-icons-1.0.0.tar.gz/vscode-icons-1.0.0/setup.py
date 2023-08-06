from setuptools import setup, find_namespace_packages
from pathlib import Path

from vscode_icons import __version__

# README FILE CONTENT
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='vscode-icons',
    version=__version__,
    description='Django app to provide vscode icons for web application.',

    long_description=long_description,
    long_description_content_type='text/markdown',
    # url='https://hello.com',

    author='Tahir Rafique',
    author_email='tahirrafiqueasad@gmail.com',
    license='MIT',

    packages=find_namespace_packages(),
    package_data={
        "": ["*.html", "*.css", "*.js", "*.svg", "*.json"],
    },
    install_requires=[
        'django>=3.2.10'
    ],

    keywords=["vscode", "icons", "vscode icons", "django icons"],
    classifiers=[
        "Framework :: Django :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
    ]
)