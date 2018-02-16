"""
Read all html meta tags that comply with a scheme
(i.e., og: for opengraph, twitter, govuk etc.).
"""
from __future__ import absolute_import
import re
import requests
from sys import argv
from bs4 import BeautifulSoup
from functools import singledispatch
from metatron.schemas import SCHEMAS
from pprint import pprint


# a single dispatch to normalise schema argument into a list
@singledispatch
def _schemas(schemas):
    return schemas


@_schemas.register(str) # noqa
def _(schemas):
    return [schemas]


def add_schema_spec(spec):
    """
    Register a custom schema
    """
    if not validate_schema_spec(spec):
        raise Exception('Invalid schema spec. name, attribute and value keys are required')
    spec_tag = spec.get('name')
    SCHEMAS[spec_tag] = spec


def validate_schema_spec(spec):
    return all([key in spec for key in ['name', 'attribute', 'value']])


class Metatron(dict):
    def __init__(self, url=None, content=None, schemas=None, schema_spec=None, **kwargs):
        if not url and not content:
            raise Exception('Either url or content are required')
        self.url = url
        self.content = content
        self.schemas = schemas or ''
        self.last_tag = None
        if schema_spec:
            add_schema_spec(schema_spec)
        self.schemas = _schemas(self.schemas)
        super().__init__(**kwargs)

    def get_content(self):
        """
        Retrieve the content, either by fetching a url content provided
        as input
        """
        if self.url:
            response = requests.get(self.url)
            self.content = response.text
        return self.content

    def get_schema_regex(self, schema):
        """
        Schema regular expression for opengraph (og:) or
        twitter cards, etc.
        """
        if schema:
            return r'{0}:([\w:]+)'.format(schema)
        else:
            return r'([\w]+[^:])'

    def fetch_meta_tags(self):
        """
        Fetch meta tags from the source url or provided content
        """
        content = self.get_content()
        soup = BeautifulSoup(content, 'html.parser')
        tags = {}
        for schema in self.schemas:
            _spec = SCHEMAS[schema]
            schema_regex = self.get_schema_regex(schema)
            find_attrs = {_spec['attribute']: re.compile(schema_regex)}
            tags[schema] = soup.find_all('meta', attrs=find_attrs)
        return tags

    def name_path(self, tag, spec):
        """
        Extract the path, minus the schema, as a list:
        From:
            <meta property="og:image:secure_url" .../>
        To:
            ['image', 'secure_url']
        """
        meta_name = tag[spec['attribute']].split(spec.get('separator', ':'))
        if spec.get('name', '') in meta_name:
            meta_name.remove(spec.get('name', ''))
        return meta_name

    def tag_parts(self, tag, spec):
        meta_name = self.name_path(tag, spec)
        root = meta_name[0] if len(meta_name) > 1 else None
        return meta_name, root

    def next_tag(self, tags, current_index, spec):
        """
        Return the next tag, if available, and determine it's parts,
        root name and if it is indeed a root element
        """
        new_root = False
        try:
            current_tag = self.name_path(tags[current_index], spec)
            next_tag = tags[current_index + 1]
            next_parts, next_root = self.tag_parts(next_tag, spec)
            if next_root == current_tag[0] and len(next_parts) != len(current_tag):
                new_root = True
            return next_parts, next_root, new_root
        except (IndexError, TypeError):
            return None, None, new_root

    def key_value_root(self, tag, spec, separator=None):
        """
        For a given tag/spec, return the key, its value
        and the root element if available
        """
        separator = separator or ":"
        meta_name, root = self.tag_parts(tag, spec)
        if root:
            meta_name.remove(root)
        tag_value = tag[spec['value']]
        tag_key = separator.join(meta_name)
        return tag_key, tag_value, root

    def traverse(self):
        """
        traverse the tags and generae an index of each schema
        being fetched
        """
        meta_tags = self.fetch_meta_tags()
        meta = dict(self)
        for schema, tags in meta_tags.items():
            _index = {}
            meta.setdefault(schema, {})
            _spec = SCHEMAS[schema]
            for i, tag in enumerate(tags):
                key, value, root = self.key_value_root(tag, _spec)
                next_tag, next_root, new_root = self.next_tag(tags, i, _spec)
                if new_root and next_root:
                    if next_root in _index:
                        _index[next_root].append({key: value})
                    else:
                        _index[next_root] = [{key: value}]
                elif not root and key in _index:
                    _index[key].append({key: value})
                else:
                    _key = root or key
                    _index.setdefault(_key, [{}])
                    _index[_key][len(_index[_key]) - 1].update({key: value})
            self.reduce(schema, _index)

    def reduce(self, schema, index):
        """
        Reduce the index into a more compact structure:
            list of length 1 updates the top level schema dict
                if the value is not a dict
                otherwise set the root to that value
            list of length over 1 sets the value of the schema dict
                as reduced strings if the length of each dict is 1
                as is otherwise
        """
        self.setdefault(schema, {})
        for key, value in index.items():
            if len(value) == 1:
                if isinstance(value[0], dict) and len(list(value[0].keys())) > 1:
                    self[schema][key] = value[0]
                else:
                    self[schema].update(value[0])
            elif len(value) > 1:
                if all([len(list(item.keys())) == 1 for item in value]):
                    self[schema][key] = [item[key] for item in value]
                else:
                    self[schema][key] = value


if __name__ == '__main__':
    arg_count = len(argv)
    if arg_count > 1:
        url = argv[1]
        schemas = argv[2] if arg_count > 2 else []
        print("Getting: {0} (schema: {1})".format(url, schemas))
        mt = Metatron(url=url, schemas=schemas)
        mt.traverse()
        pprint(mt)
