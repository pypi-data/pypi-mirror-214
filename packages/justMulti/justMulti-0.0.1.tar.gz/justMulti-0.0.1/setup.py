from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Parse html strings'
LONG_DESCRIPTION = 'Parse html strings and remove boilerplate material while extracting useful text/images/video/audio.'

# Setting up
setup(
    name="justMulti",
    version=VERSION,
    author="Vrushank Desai",
    author_email="<vrushdesai0@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['lxml'],
    keywords=['html', 'parsing'],
)