.. image:: https://badge.fury.io/py/metatron.svg
    :target: https://badge.fury.io/py/metatron

Metatron
========

HTML Meta tag parser, with emphasis on OpenGraph/Twitter Cards, and
complex (and custom) meta tag schemes. Supports Python 3.x and up.
The Metatron object extends dict, and all the meta tag data is set within it.


Installation
------------
You know the drill:

::

    pip install metatron


Straight to an example
----------------------

Simple meta tag collector
^^^^^^^^^^^^^^^^^^^^^^^^^

This example collects top level meta tags without a schema:

::

    > mt = Metatron(url='https://www.bbc.co.uk')
    > mt.traverse()

    {
        'x-country': 'gb',
        'x-audience': 'Domestic',
        'CPS_AUDIENCE': 'Domestic',
        'CPS_CHANGEQUEUEID': '115204091',
        'theme-color': 'bb1919',
        'msapplication-TileColor': '#bb1919'
    }

    > mt['x-country']
    > 'gb'

Collect structures OpenGraph meta tags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    > mt = Metatron(url='https://www.bbc.co.uk', schemas=['og'])
    > mt.traverse()

    {
        'og': {
            'title': 'Home - BBC News',
            'description': 'Visit BBC News for up-to-the-minute news....',
            'site_name': 'BBC News',
            'locale': 'en_GB',
            'article': {
                'author': 'https://www.facebook.com/bbcnews',
                'section': 'Home'
            },
            'url': 'http://www.bbc.co.uk/news',
            'image': '//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/bbc_news_logo.png'
        }
    }

Supports opengraph arrays (and can receive content as input)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    > content = """
        <meta property="og:title" content="First title tag" />
        <meta property="og:title" content="Second title tag" />
        <meta property="og:description" content="description tag" />
        <meta property="og:image" content="http://example.com/image.jpg" />
        <meta property="og:image:secure_url" content="https://secure.example.com/image.jpg" />
        <meta property="og:image:type" content="image/jpeg" />
        <meta property="og:image:width" content="400" />
        <meta property="og:image:height" content="300" />
        <meta property="og:image:alt" content="First image description" />
        <meta property="og:image" content="http://example.com/image2.jpg" />
        <meta property="og:image:secure_url" content="https://secure.example.com/image.jpg" />
        <meta property="og:image:type" content="image/jpeg" />
        <meta property="og:image:width" content="500" />
        <meta property="og:image:height" content="600" />
        <meta property="og:image:alt" content="Second image description" />
    """

    > mt = Metatron(content=content, schemas=['og'])
    > mt.traverse()

    {
        'og': {
            'description': 'description tag',
            'image': [
                {
                    'alt': 'First image descriptoin',
                    'height': '300',
                    'image': 'http://example.com/image.jpg',
                    'secure_url': 'https://secure.example.com/image.jpg',
                    'type': 'image/jpeg',
                    'width': '400'
                },
                {
                    'alt': 'A shiny green apple with a bite taken out',
                    'height': '600',
                    'image': 'http://example.com/image2.jpg',
                    'secure_url': 'https://secure.example.com/ogp.jpg',
                    'type': 'image/jpeg',
                    'width': '500'
                }
            ],
            'title': [
                'First title tag',
                'Second title tag'
            ]
        }
    }

Add your own meta tag schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can provide Metatron with your own meta tag schema spec:
::
    > from metatron import add_schema_spec
    > my_spec = {
        'name': 'boom',
        'attribute': 'name',
        'value': 'value'
    }
    > add_schema_spec(my_spec)

You can then parse tags like:
::
    <meta name="boom:title" value="Boom title" />
    <meta name="boom:description" value="Boom description" />

Using
::
    > mt = Metatron(url='http://example.com', schemas=['boom'])
    > mt.traverse()
    > {
        'boom': {
            'title': 'Boom title',
            'description': 'Boom description'
        }
    }

Can run from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ make run URL=http://bbc.co.uk/news SCHEMA=og

    or

    $ python -m metatron.metatron http://bbc.co.uk/news og

    $ Getting: http://bbc.co.uk/news (schemas: og)
    {'og': {'description': 'Visit BBC News for up-to-the-minute news, breaking '
                       'news, video, audio and feature stories. BBC News '
                       'provides trusted World and UK news as well as local '
                       'and regional perspectives. Also entertainment, '
                       'business, science, technology and health news.',
        'image': '//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.2.1/bbc_news_logo.png',
        'locale': 'en_GB',
        'section': 'Home',
        'site_name': 'BBC News',
        'title': 'Home - BBC News',
        'type': 'website',
        'url': 'http://www.bbc.co.uk/news'}}

Dependencies
^^^^^^^^^^^^

-  requests
-  beautifulsoup4
