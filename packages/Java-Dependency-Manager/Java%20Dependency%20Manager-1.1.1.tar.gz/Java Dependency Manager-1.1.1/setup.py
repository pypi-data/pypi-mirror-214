from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Java Dependency Manager',
    version='1.1.1',
    packages=['javadepsmanager'],
    entry_points={
        'console_scripts': [
            'jdm=javadepsmanager.command_line:main'
        ]
    },
    install_requires=[
        'requests==2.31.0',
    ],
    author='Repala Nagaraju',
    author_email='nagarajrepala@gmail.com',
    description='Generates Dependency tree for any java project also compares dependencies between two versions, use jdm in commandline to use this tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nagaraju6242/javadepsmanager',
    license='MIT',
    project_urls={
        'Source Code': 'https://github.com/Nagaraju6242/javadepsmanager',
        'Tracker': 'https://github.com/Nagaraju6242/javadepsmanager/issues',
    },
)
