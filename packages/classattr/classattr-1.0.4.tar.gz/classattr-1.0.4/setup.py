import setuptools
import classattr

setuptools.setup(
    name = 'classattr',
    version = classattr.__version__,
    author = classattr.__author__,
    url = 'https://framagit.org/makeforartandscience/classattr',
    license = classattr.__license__,
    description = 'classattr provides tools to manage class and object attributes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['classattr'],
    install_requires=[],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
