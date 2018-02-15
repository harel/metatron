# metatron
HTML Meta tag parser, with emphasis on OpenGraph/Twitter Cards, and complex meta tag schemes.
Supports Python 3.x and up.


## Straight to an example

#### Simple meta tag collector

This example collects top level meta tags without a schema:

```
Metatron(url='https://www.bbc.co.uk')
{
    'x-country': 'gb',
    'x-audience': 'Domestic',
    'CPS_AUDIENCE': 'Domestic',
    'CPS_CHANGEQUEUEID': '115204091',
    'theme-color': 'bb1919',
    'msapplication-TileColor': '#bb1919'
}
```

#### Collect structures OpenGraph meta tags
```
Metatron(url='https://www.bbc.co.uk', schemas=['og'])
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
```

