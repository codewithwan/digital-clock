from setuptools import setup, find_packages
from pathlib import Path

VERSION = '1.0.0'
DESCRIPTION = 'Library Digital Clock menyediakan kemampuan untuk menampilkan jam digital yang dapat disesuaikan dengan mudah dalam aplikasi berbasis Tkinter.'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="digital-clock",
    version=VERSION,
    author="codewithwan",
    author_email="<codewithwan@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/codewithwan/digital-clock',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['Digital', 'Clock'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
