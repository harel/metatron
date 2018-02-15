import unittest
from metatron import Metatron, add_schema_spec
from metatron.schemas import SCHEMAS


class TestMetatron(unittest.TestCase):
    def test_opengraph_nested(self):
        """
        {
            'image': {
                'value': 'http://example.com/ogp.jpg',
                'secure_url: 'https://secure.example.com/ogp.jpg',
            }
        }
        """
        content = """
            <meta name="description" content="Test Meta" />
            <meta property="someprop" content="Test Prop Value" />
            <meta property="og:title" content="The Two Image Shop" />
            <meta property="og:description" content="Its a shop with two images" />
            <meta property="og:image" content="http://example.com/ogp.jpg" />
            <meta property="og:image:secure_url" content="https://secure.example.com/ogp.jpg" />
            <meta property="og:image:type" content="image/jpeg" />
            <meta property="og:image:width" content="400" />
            <meta property="og:image:height" content="300" />
            <meta property="og:image:alt" content="A shiny red apple with a bite taken out" />
        """
        mt = Metatron(content=content, schemas=['og'])
        mt.traverse()
        assert mt['og']['image']['image'] == 'http://example.com/ogp.jpg'
        assert mt['og']['image']['secure_url'] == 'https://secure.example.com/ogp.jpg'


    def test_opengraph_nested_array(self):
        content = """
            <meta name="description" content="Test Meta" />
            <meta property="someprop" content="Test Prop Value" />
            <meta property="og:title" content="The Two Image Shop" />
            <meta property="og:title" content="The Two Image Store" />
            <meta property="og:description" content="Its a shop with two images" />
            <meta property="og:image" content="http://example.com/ogp.jpg" />
            <meta property="og:image:secure_url" content="https://secure.example.com/ogp.jpg" />
            <meta property="og:image:type" content="image/jpeg" />
            <meta property="og:image:width" content="400" />
            <meta property="og:image:height" content="300" />
            <meta property="og:image:alt" content="A shiny g apple with a bite taken out" />
            <meta property="og:image" content="http://example.com/ogp222.jpg" />
            <meta property="og:image:secure_url" content="https://secure.example.com/ogp.jpg" />
            <meta property="og:image:type" content="image/jpeg" />
            <meta property="og:image:width" content="500" />
            <meta property="og:image:height" content="600" />
            <meta property="og:image:alt" content="A shiny green apple with a bite taken out" />
        """
        mt = Metatron(content=content, schemas=['og'])
        mt.traverse()
        assert len(mt['og']['image']) == 2
        assert mt['og']['image'][0]['image'] == 'http://example.com/ogp.jpg'
        assert mt['og']['image'][0]['secure_url'] == 'https://secure.example.com/ogp.jpg'
        assert len(mt['og']['title']) == 2
        assert mt['og']['title'][1] == 'The Two Image Store'
        assert mt['og']['image'][1]['width'] == '500'

    def test_opengraph_array(self):
        content = """
            <meta name="description" content="Test Meta" />
            <meta property="someprop" content="Test Prop Value" />
            <meta property="og:image" content="http://example.com/ogp1.jpg" />
            <meta property="og:image:secure_url" content="https://secure.example.com/ogp1.jpg" />
            <meta property="og:image" content="http://example.com/ogp2.jpg" />
            <meta property="og:image:secure_url" content="https://secure.example.com/ogp2.jpg" />

        """
        mt = Metatron(content=content, schemas=['og'])
        mt.traverse()
        assert len(mt['og']['image']) == 2
        assert mt['og']['image'][0]['image'] == 'http://example.com/ogp1.jpg'


    def test_twitter_card_and_opengraph(self):
        """
        Collect both opengraph and twitter card schemas
        """
        content = """
            <meta property="og:title" content="Home - BBC News">
            <meta property="og:type" content="website">
            <meta property="og:description" content="Visit BBC News for up-to-the-minute news, breaking news, video, audio and feature stories. BBC News provides trusted World and UK news as well as local and regional perspectives. Also entertainment, business, science, technology and health news.">
            <meta property="og:site_name" content="BBC News">
            <meta property="og:locale" content="en_GB">
            <meta property="og:article:author" content="https://www.facebook.com/bbcnews">
            <meta property="og:article:section" content="Home">
            <meta property="og:url" content="http://www.bbc.co.uk/news">
            <meta property="og:image" content="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/bbc_news_logo.png">

            <meta name="twitter:card" content="summary_large_image">
            <meta name="twitter:site" content="@BBCNews">
            <meta name="twitter:title" content="Home - BBC News">
            <meta name="twitter:description" content="Visit BBC News for up-to-the-minute news, breaking news, video, audio and feature stories. BBC News provides trusted World and UK news as well as local and regional perspectives. Also entertainment, business, science, technology and health news.">
            <meta name="twitter:creator" content="@BBCNews">
            <meta name="twitter:image:src" content="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/bbc_news_logo.png">
            <meta name="twitter:image:alt" content="BBC News">
            <meta name="twitter:domain" content="www.bbc.co.uk">

            <link rel="apple-touch-icon-precomposed" sizes="57x57" href="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/apple-touch-icon-57x57-precomposed.png">
            <link rel="apple-touch-icon-precomposed" sizes="72x72" href="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/apple-touch-icon-72x72-precomposed.png">
            <link rel="apple-touch-icon-precomposed" sizes="114x114" href="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/apple-touch-icon-114x114-precomposed.png">
            <link rel="apple-touch-icon-precomposed" sizes="144x144" href="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/apple-touch-icon.png">
            <link rel="apple-touch-icon" href="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/apple-touch-icon.png">
            <meta name="msapplication-TileImage" content="//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/windows-eight-icon-144x144.png">

            <meta name="theme-color" content="#bb1919">
            <meta name="msapplication-TileColor" content="#bb1919">

            <meta name="x-country" content="gb">
            <meta name="x-audience" content="Domestic">
            <meta name="CPS_AUDIENCE" content="Domestic">
            <meta name="CPS_CHANGEQUEUEID" content="115204091">
        """
        mt = Metatron(content=content, schemas=['og', 'twitter'])
        mt.traverse()
        assert 'twitter' in mt
        assert 'og' in mt
        assert mt['og']['image'] == '//m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/2.1.0/bbc_news_logo.png'
        assert mt['twitter']['domain'] == 'www.bbc.co.uk'
        assert mt['twitter']['description'].startswith('Visit BBC News')

    def test_simple_meta(self):
        """
        Test that simple meta tags are collected when no schema is provided
        """
        content = """
            <meta name="theme-color" content="#bb1919">
            <meta name="msapplication-TileColor" content="#bb1919">

            <meta name="x-country" content="gb">
            <meta name="x-audience" content="Domestic">
            <meta name="CPS_AUDIENCE" content="Domestic">
            <meta name="CPS_CHANGEQUEUEID" content="115204091">
        """
        mt = Metatron(content=content)
        mt.traverse()
        assert mt['']['CPS_CHANGEQUEUEID'] == '115204091'
        assert mt['']['x-country'] == 'gb'

    def test_add_schema(self):
        schema = {
            'name': 'test',
            'attribute': 'test',
            'value': 'test'
        }
        add_schema_spec(schema)
        assert 'test' in SCHEMAS
        assert SCHEMAS['test']['name'] == 'test'



if __name__ == '__main__':
    unittest.main()
