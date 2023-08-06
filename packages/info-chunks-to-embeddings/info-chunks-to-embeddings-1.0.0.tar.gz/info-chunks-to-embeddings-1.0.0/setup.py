
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="info-chunks-to-embeddings",
    version="1.0.0",
    packages=find_packages(),
    py_modules=['info_chunks_to_embeddings'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'info_chunks_to_embeddings = info_chunks_to_embeddings:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
