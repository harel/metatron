from distutils.core import setup
from metatron.version import __version__


setup(
    name='metatron',
    version=__version__,
    description='HTML Meta tag parser',
    long_description='Metatron is a Python 3 (only) HTML meta tag parser. It has an emphasis'
                     'on complex meta tag structures, and was created to parse OpenGraph'
                     'and Twitter Card meta tags, including handling of arrays, although'
                     'it can handle any meta tag scheme.',
    author='Harel Malka',
    author_email='harel@harelmalka.com',
    url='https://github.com/harel/metatron',
    download_url='https://github.com/harel/metatron/archive/0.1.tar.gz',
    keywords=['html', 'meta', 'parser', 'opengraph', 'twittercard'],
    install_requires=[
        'beautifulsoup4==4.6.0',
        'requests==2.18.4',
    ],
    license='MIT',
    packages=['metatron', 'metatron.tests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'Programming Language :: Python :: 3.5',
    ]
)
