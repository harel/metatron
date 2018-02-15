from setuptools import setup, find_packages
from codecs import open
from os import path
from metatron.version import __version__

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='metatron',
    version=__version__,
    description='Python 3 HTML meta tag parser, with emphasis on complex meta tag structures '
                'with support for OpenGraph and Twitter Card tags, including array handling',
    long_description=long_description,
    author='Harel Malka',
    author_email='harel@harelmalka.com',
    url='https://github.com/harel/metatron',
    download_url='https://github.com/harel/metatron/archive/0.1.tar.gz',
    keywords='html meta parser opengraph twittercard',
    install_requires=[
        'beautifulsoup4==4.6.0',
        'requests==2.18.4',
    ],
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'Programming Language :: Python :: 3.5',
    ]
)
